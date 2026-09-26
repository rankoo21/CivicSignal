import json, pytest
from harness import load, UserError

@pytest.fixture
def env(): return load('civic_signal.py','CivicSignal')

def test_open_verify_close(env):
    _, c, _, q, w, _ = env
    c.open_incident('INC-1','Payments API','Payments are intermittently failing for some users.','https://status.example/inc','https://postmortem.example/inc','https://advisory.example/inc')
    bodies=['status says impact is resolved and the service is operating normally','postmortem says the incident is closed after mitigation and follow-up','advisory confirms recovery and gives the next monitoring step']
    w.extend(bodies + bodies)
    q.extend(['{"status":"RESOLVED","summary":"The incident is closed.","next_step":"Monitor the next release."}'] * 2)
    c.verify_incident('inc-1')
    c.close_incident('INC-1')
    r=json.loads(c.get_incident('0xowner','INC-1'))
    assert r['state']=='CLOSED' and r['signal']=='RESOLVED' and len(r['digests'])==3

def test_distinct_hosts_and_close_guard(env):
    _, c, _, _, _, _ = env
    with pytest.raises(UserError): c.open_incident('INC-1','API','This incident summary is long enough for validation.','https://same.example/a','https://same.example/b','https://same.example/c')
    c.open_incident('INC-2','API','This incident summary is long enough for validation.','https://status.example/a','https://postmortem.example/b','https://advisory.example/c')
    with pytest.raises(UserError): c.close_incident('INC-2')

def test_bad_consensus_fails(env):
    _, c, _, q, w, _ = env
    c.open_incident('INC-3','API','This incident summary is long enough for validation.','https://status.example/a','https://postmortem.example/b','https://advisory.example/c')
    w.extend(['status body is sufficiently long for testing','postmortem body is sufficiently long for testing','advisory body is sufficiently long for testing'])
    q.append('{}')
    with pytest.raises((ValueError,UserError)): c.verify_incident('INC-3')
