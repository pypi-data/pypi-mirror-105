import sys

EXCLUSIONS = {'<'}          # Ignore <listcomp>, etc. in the function name.
CALL_EVENT_LIST = []


class FileFilter():
    @staticmethod
    def filter(filename):
        return True

    @staticmethod
    def old_filter(filename):
        return True


class CallTrace():

    def __init__(self, filter_func=None):
        self.filter_func = filter_func

    def __enter__(self):
        self.start()
        self.tracefunc.stack_level = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.output()

    @staticmethod
    def tracefunc(frame, event, arg):
        if event == "call":
            CallTrace.tracefunc.stack_level += 1

            unique_id = frame.f_code.co_filename + str(frame.f_lineno)
            if unique_id in CallTrace.tracefunc.memorized:
                return

            # Part of filename MUST be in white list.
            if 'self' in frame.f_locals:
                class_name = frame.f_locals['self'].__class__.__name__
                func_name = class_name + '.' + frame.f_code.co_name
            else:
                func_name = frame.f_code.co_name

            if func_name == 'CallTrace.__exit__' or func_name == 'CallTrace.stop':
                return

            func_name = '{indent}{name}'.format(
                indent=CallTrace.tracefunc.stack_level * 2 * '-', name=func_name)

            if not FileFilter.filter(frame.f_code.co_filename):
                return

            frame_back = frame.f_back  # 获取调用函数时的信息
            txt = '{: <40} # {}, {}, {}, {}'.format(
                func_name, frame.f_code.co_filename, frame.f_lineno, frame_back.f_code.co_filename, frame_back.f_lineno)


            CALL_EVENT_LIST.append(txt)
            CallTrace.tracefunc.memorized.add(unique_id)

        elif event == "return":
            CallTrace.tracefunc.stack_level -= 1


    def start(self, filter_func=None):
        if filter_func:
            FileFilter.filter = filter_func
        elif self.filter_func:
            FileFilter.filter = self.filter_func

        self.tracefunc.memorized = set()
        self.tracefunc.stack_level = 0
        CALL_EVENT_LIST.clear()
        sys.setprofile(self.tracefunc)

    def stop(self):
        def do_nothing(frame, event, arg):
            pass

        FileFilter.filter = FileFilter.old_filter
        sys.setprofile(do_nothing)

    def output(self):
        for text in CALL_EVENT_LIST:
            print(text)

        CALL_EVENT_LIST.clear()