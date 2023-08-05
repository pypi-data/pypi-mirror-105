import logging
from typing import List

from sacrerouge.data import EvalInstance
from sacrerouge.data.dataset_readers import DatasetReader
from sacrerouge.data.fields import Fields, SummaryField
from sacrerouge.io import JsonlReader

logger = logging.getLogger(__name__)


@DatasetReader.register('summary-only')
class SummaryOnlyDatasetReader(DatasetReader):
    def read(self, input_jsonl: str) -> List[EvalInstance]:
        logger.info(f'Loading evaluation instances from {input_jsonl}')
        instances = []
        with JsonlReader(input_jsonl) as f:
            for data in f:
                fields = {}
                fields['summary'] = SummaryField(data['summary']['text'])
                fields = Fields(fields)

                instance = EvalInstance(
                    data['instance_id'],
                    data['summarizer_id'],
                    data['summarizer_type'],
                    fields
                )
                instances.append(instance)

            logger.info(f'Loaded {len(instances)} instances')
            return instances
