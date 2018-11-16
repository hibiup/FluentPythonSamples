import sys
import getopt
import argparse


if __name__ == "__main__":
    """ Test sys.args """
    print(f"Length of argument: {len(sys.argv)}, {sys.argv[0]}, {sys.argv[1]}, {sys.argv[2]}, and the rest: {sys.argv[3:]}")

    """ Test getopt """
    getopt.getopt
    shortOptions = "pt:a"                      # 冒号表示 t 必须有值
    longOptions = ["port", "timeout=", "aaa"]  # 等号表示 timeout 必须有值
    arguments, values = getopt.getopt(sys.argv[1:], shortOptions, longOptions)
    print(arguments, values)

    """ Test argparse """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', "--port", help='Port', type=int, default=0)
    parser.add_argument('-t', "--timeout", help='Timeout', type=int, default=0)
    args, unknown = parser.parse_known_args()

    port = args.port
    timeout = args.timeout
    print(args, port, timeout, unknown)
