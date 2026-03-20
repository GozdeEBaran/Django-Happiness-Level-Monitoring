import logging
import traceback
from django.conf import settings


class StackInfoHandler(logging.StreamHandler):  # coverage: omit
    def emit(self, record):
        try:
            self.msg_detail = self.format(record)
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

        trace = traceback.format_stack()
        stack1 = [str(row) for row in trace]
        stack2 = [s for s in stack1 if settings.BASE_DIR in s and 'format_stack' not in s]
        if stack2:
            stack4 = ''.join(stack2[-3:])
            stack5 = f">>>> {self.terminator} {''.join(stack4)}"
            self.stream.write(stack5)
            self.stream.write(self.terminator)
            self.stream.write(self.msg_detail)
            self.stream.write(self.terminator)
            self.flush()
