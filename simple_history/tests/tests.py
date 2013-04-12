from datetime import datetime, timedelta
from django.test import TestCase

from .models import Poll


today = datetime(2021, 1, 1, 10, 0)
tomorrow = today + timedelta(days=1)


class HistoricalRecordsTest(TestCase):

    def assertDatetimesEqual(self, time1, time2):
        self.assertAlmostEqual(time1, time2, delta=timedelta(seconds=2))

    def assertRecordValues(self, record, values_dict):
        for key, value in values_dict.items():
            self.assertEqual(getattr(record, key), value)

    def test_create(self):
        p = Poll(question="what's up?", pub_date=today)
        p.save()
        history = p.history.all()
        record, = history
        self.assertRecordValues(record, {
            'question': "what's up?",
            'pub_date': today,
            'id': p.id,
            'history_type': "+"
        })

    def test_update(self):
        Poll.objects.create(question="what's up?", pub_date=today)
        p = Poll.objects.get()
        p.pub_date = tomorrow
        p.save()
        history = p.history.all()
        update_record, create_record = history
        self.assertRecordValues(create_record, {
            'question': "what's up?",
            'pub_date': today,
            'id': p.id,
            'history_type': "+"
        })
        self.assertRecordValues(update_record, {
            'question': "what's up?",
            'pub_date': tomorrow,
            'id': p.id,
            'history_type': "~"
        })

    def test_delete(self):
        p = Poll.objects.create(question="what's up?", pub_date=today)
        poll_id = p.id
        p.delete()
        history = Poll.history.all()
        delete_record, create_record = history
        self.assertRecordValues(create_record, {
            'question': "what's up?",
            'pub_date': today,
            'id': poll_id,
            'history_type': "+"
        })
        self.assertRecordValues(delete_record, {
            'question': "what's up?",
            'pub_date': today,
            'id': poll_id,
            'history_type': "-"
        })
