import asyncio
import ipaddress
from pathlib import Path

import aiofiles
import pytest
from aiosmtpd.smtp import Session
from apscheduler.schedulers.base import BaseScheduler
from asynctest import MagicMock, CoroutineMock

import ModernRelay.relay
from ModernRelay.agents import DeliveryAgentBase
from ModernRelay.file_manager import FileManager


class TestRelay:

    @pytest.fixture
    def session_anon(self, event_loop):
        sess = Session(loop=event_loop)
        sess.peer = ('172.16.128.64', 64160)
        sess.extended_smtp = True
        return sess

    @pytest.fixture
    def session_auth(self, event_loop):
        sess = Session(loop=event_loop)
        sess.peer = ('172.16.129.64', 64160)
        sess.extended_smtp = True
        return sess

    @pytest.fixture
    def mocked_agent(self):
        def inner(ret=True):
            DeliveryAgentBase.__abstractmethods__ = set()

            class DummyDeliveryAgent(DeliveryAgentBase):
                pass

            mocked = MagicMock(DummyDeliveryAgent())
            mocked.send_mail.return_value = asyncio.Future()
            mocked.send_mail.return_value.set_result(ret)
            return mocked

        return inner

    @pytest.fixture
    def peer_map(self):
        def inner(agent):
            peer_map = {
                ipaddress.ip_network('172.16.128.0/24'): {
                    'authenticated': False,
                    'agent': agent,
                    'destinations': 'all'
                },
                ipaddress.ip_network('172.16.129.0/24'): {
                    'authenticated': True,
                    'agent': agent,
                    'destinations': ['example.com', 'google.com']
                }
            }
            return peer_map

        return inner

    @pytest.fixture
    def relay(self, mocked_agent, peer_map):
        return ModernRelay.relay.ModernRelay(peer_map(mocked_agent()))

    @pytest.fixture
    def relay_with_file_manager(self, mocked_agent, peer_map):
        return ModernRelay.relay.ModernRelay(peer_map, FileManager(False))

    @pytest.mark.asyncio
    async def test_ehlo(self, relay, session_anon, envelope):
        hostname = '[172.16.128.64]'
        responses = ['250-HERMES', '250-SIZE 33554432', '250-8BITMIME', '250-SMTPUTF8', '250 HELP']
        assert await relay.handle_EHLO(None, session_anon, envelope, hostname, responses) == responses
        assert session_anon.host_name == hostname

    @pytest.mark.asyncio
    async def test_mail_anon_auth(self, relay, session_anon, envelope):
        address = 'brett@example.com'
        mail_options = ['SIZE=761132']
        result = await relay.handle_MAIL(None, session_anon, envelope, address, mail_options)

        assert result == "250 OK"
        assert hasattr(session_anon, 'mr_agent')
        assert hasattr(session_anon, 'mr_destinations')
        assert isinstance(session_anon.mr_agent, MagicMock)
        assert envelope.mail_from == address
        assert envelope.mail_options == mail_options

    @pytest.mark.asyncio
    async def test_mail_good_auth(self, relay, session_auth, envelope):
        address = 'brett@example.com'
        mail_options = ['SIZE=761132']
        session_auth.authenticated = True
        result = await relay.handle_MAIL(None, session_auth, envelope, address, mail_options)

        assert result == "250 OK"
        assert hasattr(session_auth, 'mr_agent')
        assert hasattr(session_auth, 'mr_destinations')
        assert isinstance(session_auth.mr_agent, MagicMock)
        assert envelope.mail_from == address
        assert envelope.mail_options == mail_options

    @pytest.mark.asyncio
    async def test_mail_bad_auth(self, relay, session_auth, envelope):
        address = 'brett@example.com'
        mail_options = ['SIZE=761132']
        session_auth.authenticated = False
        result = await relay.handle_MAIL(None, session_auth, envelope, address, mail_options)

        assert result == "530 5.7.0 Authentication required"

    @pytest.mark.asyncio
    async def test_mail_peer_denied_relay(self, relay, session_anon, envelope):
        address = 'brett@example.com'
        mail_options = ['SIZE=761132']
        session_anon.peer = ('192.168.1.2', 69160)
        result = await relay.handle_MAIL(None, session_anon, envelope, address, mail_options)

        assert result == "550 Mail from this IP address is refused"

    @pytest.mark.asyncio
    async def test_rcpt_allow_all(self, relay, session_anon, envelope):
        address = 'brett@example.com'
        rcpt_options = ['test-option']
        session_anon.mr_destinations = "all"
        result = await relay.handle_RCPT(None, session_anon, envelope, address, rcpt_options)

        assert result == "250 OK"
        assert address in envelope.rcpt_tos
        assert set(envelope.rcpt_options).issubset(rcpt_options)

    @pytest.mark.asyncio
    async def test_rcpt_str_destinations_not_all(self, relay, session_anon, envelope):
        address = 'brett@example.com'
        rcpt_options = []
        session_anon.mr_destinations = "oops-this-is-a-typo"
        result = await relay.handle_RCPT(None, session_anon, envelope, address, rcpt_options)

        assert result == "550 Error with allowed destinations"

    @pytest.mark.asyncio
    async def test_rcpt_list_destinations_allowed_relay(self, relay, session_anon, envelope):
        address = 'brett@example.com'
        rcpt_options = ['test-option']
        session_anon.mr_destinations = ['example.com', 'google.com']
        result = await relay.handle_RCPT(None, session_anon, envelope, address, rcpt_options)

        assert result == "250 OK"
        assert address in envelope.rcpt_tos
        assert set(envelope.rcpt_options).issubset(rcpt_options)

    @pytest.mark.asyncio
    async def test_rcpt_list_destinations_denied_relay(self, relay, session_anon, envelope):
        address = 'brett@bing.com'
        rcpt_options = []
        session_anon.mr_destinations = ['example.com', 'google.com']
        result = await relay.handle_RCPT(None, session_anon, envelope, address, rcpt_options)

        assert result == "550 Domain is not allowed to be relayed"

    @pytest.mark.asyncio
    async def test_data_no_agent(self, relay, session_anon, envelope):
        result = await relay.handle_DATA(None, session_anon, envelope)

        assert result == "500 Failed to match session with delivery agent"

    @pytest.mark.asyncio
    async def test_data_with_attachment(self, relay, session_anon, envelope_attachment, mocked_agent):
        session_anon.mr_agent = mocked_agent()

        result = await relay.handle_DATA(None, session_anon, envelope_attachment)

        assert result == "250 Message accepted for delivery"

    @pytest.mark.asyncio
    async def test_data_with_attachment_failure(self, relay, session_anon, envelope_attachment, mocked_agent):
        session_anon.mr_agent = mocked_agent(False)

        result = await relay.handle_DATA(None, session_anon, envelope_attachment)

        assert result == "500 Delivery agent failed"

    @pytest.mark.asyncio
    async def test_data_with_attachment_schedule_after_failure(self, relay_with_file_manager, session_anon,
                                                               envelope_attachment, mocked_agent, cleanup_files):
        session_anon.mr_agent = mocked_agent(False)

        result = await relay_with_file_manager.handle_DATA(None, session_anon, envelope_attachment)
        spooled_files = relay_with_file_manager.file_manager.get_files()

        assert result == "500 Delivery agent failed"
        assert spooled_files
        assert len(spooled_files) == 1

    @pytest.mark.asyncio
    async def test_data_with_attachment_failure_save_file_failure(self, relay, session_anon, caplog,
                                                                  envelope_attachment, mocked_agent):
        session_anon.mr_agent = mocked_agent(False)
        relay.file_manager = MagicMock()
        relay.file_manager.save_file = CoroutineMock()
        relay.file_manager.save_file.return_value = None

        result = await relay.handle_DATA(None, session_anon, envelope_attachment)

        assert result == "500 Delivery agent failed"
        assert "Unable to save email to disk!" in caplog.text

    @pytest.mark.asyncio
    async def test_send_mail_from_disk_success(self, envelope_peer_spooled):
        file_path = MagicMock(Path)
        file_manager = MagicMock(FileManager)
        file_manager.open_file = CoroutineMock()
        file_manager.open_file.return_value = envelope_peer_spooled
        scheduler = MagicMock(BaseScheduler)
        scheduler.remove_job = MagicMock()
        session = MagicMock(Session)
        session.mr_agent = MagicMock()
        session.mr_agent.send_mail = CoroutineMock()
        session.mr_agent.send_mail.return_value = True

        result = await ModernRelay.relay.send_mail_from_disk(file_path, file_manager, scheduler, session)

        assert result
        scheduler.remove_job.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_mail_from_disk_failure(self, envelope_peer_spooled, mock_file_manager, mock_scheduler):
        session = MagicMock(Session)
        session.mr_agent = MagicMock()
        session.mr_agent.send_mail = CoroutineMock()
        session.mr_agent.send_mail.return_value = False

        result = await ModernRelay.relay.send_mail_from_disk(mock_file_manager._file_path,
                                                             mock_file_manager,
                                                             mock_scheduler,
                                                             session)

        assert result is False
        mock_scheduler.remove_job.assert_not_called()

    @pytest.mark.asyncio
    async def test_load_old_jobs_success(self, file_manager, mock_scheduler, peer_map, mocked_agent,
                                         spool, spooled_file, cleanup_files):
        async with aiofiles.open(spooled_file, 'rb') as src, \
                aiofiles.open(spool / spooled_file.name, 'wb') as dst:
            await dst.write(await src.read())
        map = peer_map(mocked_agent())
        fm = file_manager(False)

        await ModernRelay.relay.load_old_jobs(fm, map, mock_scheduler)

        mock_scheduler.add_job.assert_called_once()

    @pytest.mark.asyncio
    async def test_load_old_jobs_fail_bad_file(self, file_manager, mock_scheduler, peer_map, mocked_agent,
                                               spool, spooled_file_bad_peer, cleanup_files):
        async with aiofiles.open(spooled_file_bad_peer, 'rb') as src, \
                aiofiles.open(spool / spooled_file_bad_peer.name, 'wb') as dst:
            await dst.write(await src.read())
        map = peer_map(mocked_agent())
        fm = file_manager(False)

        await ModernRelay.relay.load_old_jobs(fm, map, mock_scheduler)

        mock_scheduler.add_job.assert_not_called()

    @pytest.mark.asyncio
    async def test_load_old_jobs_fail_peer_not_in_map(self, file_manager, mock_scheduler, peer_map, mocked_agent,
                                                      spool, spooled_file_peer_130, cleanup_files):
        async with aiofiles.open(spooled_file_peer_130, 'rb') as src, \
                aiofiles.open(spool / spooled_file_peer_130.name, 'wb') as dst:
            await dst.write(await src.read())
        map = peer_map(mocked_agent())
        fm = file_manager(False)

        await ModernRelay.relay.load_old_jobs(fm, map, mock_scheduler)

        mock_scheduler.add_job.assert_not_called()
