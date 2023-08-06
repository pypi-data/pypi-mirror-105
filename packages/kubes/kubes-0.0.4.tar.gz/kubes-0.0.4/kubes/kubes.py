"""
Kubenetes CLI
"""
import argparse
import re
import os
import subprocess
import sys


class ColorTag:
    RESET = '\x1b[0m'

    RED = '\x1b[5;31;40m'
    BLUE = '\x1b[5;34;40m'
    CYAN = '\x1b[5;36;40m'
    GRAY = '\x1b[5;37;40m'
    GREEN = '\x1b[5;32;40m'
    YELLOW = '\x1b[5;33;40m'

    ON_RED = '\x1b[5;30;41m'
    ON_BLUE = '\x1b[5;30;44m'
    ON_CYAN = '\x1b[5;30;46m'
    ON_GRAY = '\x1b[5;30;47m'
    ON_GREEN = '\x1b[5;30;42m'
    ON_YELLOW = '\x1b[5;30;43m'

    RED_ON_YELLOW = '\x1b[5;31;43m'
    BLUE_ON_YELLOW = '\x1b[3;34;43m'
    GRAY_ON_CYAN = '\x1b[3;37;46m'
    GRAY_ON_RED = '\x1b[3;37;41m'
    YELLOW_ON_RED = '\x1b[5;33;41m'
    YELLOW_ON_BLUE = '\x1b[5;33;44m'


class Kubes:
    """
    usage: kubes [-h] [-i] [--command COMMAND][-l][--context CONTEXT] [--namespace NAMESPACE] [--pod POD]
                 [--log] [--follow] [--tail TAIL]
                 [--download] [--src SRC] [--dest DEST]
    """

    try:
        _TERMINAL_SIZE_WIDTH = os.get_terminal_size().columns
    except:
        _TERMINAL_SIZE_WIDTH = 90

    _FG_COLORS = [
        ColorTag.CYAN,
        ColorTag.GRAY,
        ColorTag.GREEN,
        ColorTag.YELLOW,
        ColorTag.RED,
        ColorTag.BLUE,
    ]

    _BG_COLORS = [
        ColorTag.ON_CYAN,
        ColorTag.ON_GRAY,
        ColorTag.ON_GREEN,
        ColorTag.ON_YELLOW,
        ColorTag.ON_RED,
        ColorTag.ON_BLUE,
    ]

    _PATTERN_FORM = r'[^ \t\n]+ *'
    _PATTERN_POD_LABEL = '\-[\w\d]+\-[\w\d]+$'

    _REGEX_FORM = re.compile(_PATTERN_FORM)


    @classmethod
    def _help(cls):
        print(cls.__doc__)
        sys.exit()

    @classmethod
    def _get_args(cls):
        parser = argparse.ArgumentParser()
        # ---------------- 操作 ---------------- #
        # 互動模式
        parser.add_argument(
            '-i', '--interact',
            action='store_true',
            help='Execute Container',
        )
        # 互動指令
        parser.add_argument(
            '--command',
            help='Specify Command [default value: bash]',
            type=str,
        )
        # ---------------- 操作 ---------------- #
        # 下載檔案
        parser.add_argument(
            '--download',
            action='store_true',
            help='Download File or Folder',
        )
        # 複製檔案來源路徑
        parser.add_argument(
            '--src',
            help='Specify Source',
            type=str,
        )
        # 複製檔案存放路徑
        parser.add_argument(
            '--dest',
            help='Specify Destination [default value: current location]',
            type=str,
        )
        # ---------------- 操作 ---------------- #
        # 列出當前 Namespace 下所有 Pods
        parser.add_argument(
            '-l', '--list',
            action='store_true',
            help='List the pods of the current namespace',
        )
        # ---------------- 操作Logs ---------------- #
        # 列出指定 Pod 下 logs
        parser.add_argument(
            '--log',
            action='store_true',
            help='Download File or Folder',
        )
        parser.add_argument(
            '--follow',
            action='store_true',
            help='Keep Streaming Container Logs',
        )
        parser.add_argument(
            '--tail',
            help='Track the Logs back with specific number [default value: 100]',
            type=int,
        )
        # ---------------- 指定 ---------------- #
        parser.add_argument(
            '--context',
            help='Specify Context',
            type=str,
        )
        parser.add_argument(
            '--namespace',
            help='Specify Namespace',
            type=str,
        )
        parser.add_argument(
            '--pod',
            help='Specify Pod',
            type=str,
        )
        return parser.parse_args()

    @classmethod
    def _stdout(cls, output, tag=None, end='\n'):
        header = str()
        if tag:
            badge = f' [{tag.upper()}] '
            header = f'{ColorTag.ON_CYAN}{badge:-^{cls._TERMINAL_SIZE_WIDTH}}{ColorTag.RESET}\n'
        sys.stdout.write(
            f'{header}{output}{end}'
        )

    @classmethod
    def _stderr(cls, output, tag=None, end='\n'):
        header = str()
        if tag:
            badge = f' [{tag.upper()}] '
            header = f'{ColorTag.ON_RED}{badge:-^{cls._TERMINAL_SIZE_WIDTH}}{ColorTag.RESET}\n'
        sys.stderr.write(
            f'{header}'
            f'{ColorTag.RED}{output}{ColorTag.RESET}{end}'
        )
        exit('Program has been terminated')

    @classmethod
    def _exec(cls, cmd):
        try:
            output = subprocess.check_output(
                cmd,
                stderr=subprocess.STDOUT,
                shell=True,
                timeout=10,
                universal_newlines=True,
            )
        except subprocess.CalledProcessError as e:
            cls._stderr(output=e.output, tag='error')
        else:
            return output

    @classmethod
    def _get_fg_color(cls, index):
        return cls._FG_COLORS[index % len(cls._FG_COLORS)]

    @classmethod
    def _get_bg_color(cls, index):
        return cls._BG_COLORS[index % len(cls._BG_COLORS)]

    @classmethod
    def _is_not_running(cls, text):
        if text.lower().startswith('running'):
            return True
        return False

    @classmethod
    def _format_line(cls, index, text, status_index, is_title=None):
        if status_index is not None and index == status_index and cls._is_not_running(text=text):
            return f'{ColorTag.RED}{text}{ColorTag.RESET}'
        color = cls._get_bg_color(index=index) if is_title else cls._get_fg_color(index=index)
        return f'{color}{text}{ColorTag.RESET}'

    @classmethod
    def _format_form(cls, form, has_header=False):
        """ has_header just format the 1st line(loop) """
        if len(form) == 2 and not form[1]:
            cls._stderr(output=form[0])
        status_index = None
        for index, line in enumerate(form, start=1):
            texts = cls._REGEX_FORM.findall(line)
            if not texts:
                continue
            result = str()
            for index, text in enumerate(texts):
                result += cls._format_line(index=index, text=text, status_index=status_index, is_title=has_header)
                if has_header and 'STATUS' in text:
                    status_index = index
            cls._stdout(output=result)
            has_header = False

    @classmethod
    def _list_pods(cls):
        cmd = f'kubectl get pods'
        stdout = cls._exec(cmd=cmd)
        form = stdout.split('\n')
        cls._format_form(form=form, has_header=True)

    @classmethod
    def _switch_context(cls, args):
        cmd = f'kubectl config set-context --current --namespace={args.context}'
        result = cls._exec(cmd=cmd)
        cls._stdout(output=result)

    @classmethod
    def _get_pods(cls):
        cmd = 'kubectl get pods --no-headers --output=custom-columns="NAME:.metadata.name"'
        stdout = cls._exec(cmd=cmd)
        if not stdout:
            cls._stderr(output=f'No pods in the current namespace')
        return stdout.split('\n')

    @classmethod
    def _get_pod(cls, pod_name):
        pods = cls._get_pods()
        regex = re.compile(f'{pod_name}{cls._PATTERN_POD_LABEL}')
        for pod in pods:
            if not regex.match(pod):
                continue
            return pod
        pod_info = '\n'.join(f'\t{pod}' for pod in pods)
        cls._stderr(output=f'Cannot Find <POD {pod_name}>:\n{pod_info}', tag='error')

    @classmethod
    def _download(cls, args):
        if not args.pod:
            exit(f'Missing Key: --pod')
        pod = cls._get_pod(pod_name=args.pod)
        if not args.src:
            exit(f'Missing Key: --src')
        source = args.src.lstrip('/')
        destination = args.dest or '.'
        cmd = f'kubectl cp {pod}:{source} {destination}'
        result = cls._exec(cmd=cmd)
        cls._stdout(output=result)

    @classmethod
    def _interact(cls, args):
        if not args.pod:
            exit(f'Missing Key: --pod')
        command = args.command or 'bash'
        pod = cls._get_pod(pod_name=args.pod)
        cmd = f'kubectl exec -it {pod} -- {command}'
        os.system(cmd)

    @classmethod
    def _log(cls, args):
        if not args.pod:
            exit(f'Missing Key: --pod')
        pod = cls._get_pod(pod_name=args.pod)
        if args.follow:
            """ 串流直至退出 """
            os.system(f'kubectl logs {pod} --follow')
            exit()
        tail = args.tail or 100
        cmd = f'kubectl logs --tail={tail} {pod}'
        stdout = cls._exec(cmd=cmd)
        logs = stdout.split('\n')
        for log in logs:
            if 'GET /probe' in log or 'kube-probe/1.18' in log:
                continue
            cls._stdout(output=log)

    @classmethod
    def cli(cls):
        if len(sys.argv) == 1:
            cls._help()
        args = cls._get_args()
        if args.list:
            cls._list_pods()
            exit()
        if args.log:
            cls._log(args=args)
            exit()
        if args.context:
            cls._switch_context(args=args)
            exit()
        if args.download:
            cls._download(args=args)
            exit()
        if args.interact:
            cls._interact(args=args)
            exit()

