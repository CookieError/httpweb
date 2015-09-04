import time
import urllib2
import argparse
import os
import logging
import datetime

__version__ = "0.1.0"


WEBSITE = None
DEBUG_FILE = None

start = None
end = None
time_taken = None

path = None
path2 = None

my_switch = True
CODE = None
SHOW = False

VERBOSE = False

USER_AGENT_PATH = ""
USER_AGENT = None
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"


def main():

    set_debug_file()
    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' set up the debug file')
    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' calling default_output_path')

    default_output_path()
    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' calling get_commands')
    get_commands()

    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' calling loop')
    print "Working ...."
    loop()

    if SHOW:
        logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' now calling show_results')
        show_results()

    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' end \n \n')


def set_debug_file():
    global DEBUG_FILE

    temp = os.getenv("HOME")
    temp2 = "/.mulvie/"
    temp3 = "httpweb/"
    filename = "log.txt"

    t = temp + temp2
    tt = t + temp3

    if os.path.isdir(t):
        pass
    else:
        os.mkdir(t)

    if os.path.isdir(tt):
        pass
    else:
        os.mkdir(tt)

    DEBUG_FILE = temp + temp2 + temp3 + filename

    logging.basicConfig(filename=DEBUG_FILE, filemode='a', level=logging.DEBUG)


def get_status_code(val):
    global CODE
    global WEBSITE

    WEBSITE = str(val).strip(" ")
    header = {'User-Agent': USER_AGENT}

    req = urllib2.Request(WEBSITE, None, header)
    try:
        my_http = urllib2.urlopen(req, timeout=9)
        CODE = my_http.getcode()
        logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' request was successful ' + str(CODE))
    except:
        logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' request was unsuccessful ' + str(CODE))


def read_list():
    val = []

    with open(path2) as f:
        for line in f:
            val.append(line.strip('\n'))

    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' reading from file was successful ')
    return val


def user_path():
    info = []
    try:

        with open(USER_AGENT_PATH) as af:
            for line in af:
                t = line.strip("\n")
                info.append(t.strip(" "))

        return info
    except:
        pass


def write_file(data):
    with open(path, 'a') as f:
        f.write(str(data))

    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' writing to file was successful ')


def loop():
    global start
    global end
    global time_taken
    global my_switch
    global USER_AGENT

    val = read_list()
    i = 0
    j = 0
    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' starting loop ')

    while my_switch:
        if VERBOSE:
            print "URL: " + str(WEBSITE)
            print "AGENT: " + str(USER_AGENT)

        start = time.time()

        try:
            logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' sending request to '
                          + str(WEBSITE))
            get_status_code(val[i])
            i = i + 1

        except IndexError:
            i = 0
            try:
                something = user_path()
                USER_AGENT = something[j]

            except IndexError:
                logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' indexError for USER_AGENT')
                if not USER_AGENT:
                    my_switch = False

            j = j + 1

        end = time.time()
        time_taken = end - start

        if not WEBSITE or not USER_AGENT:
            pass
        else:
            write_file("url: " + str(WEBSITE) + "\n")
            write_file("code: " + str(CODE) + "\n")
            write_file("user_agent: " + str(USER_AGENT) + "\n")
            write_file("time taken to load: " + str(time_taken) + "\n" + "\n")


def show_results():
    with open(path) as f:
        print f.read()


def default_output_path():
    global path
    home = os.getenv("HOME")
    temp_dir = "/.mulvie/"
    temp_dir2 = "httpweb/"
    temp_file = "output.txt"

    path = home + temp_dir + temp_dir2 + temp_file

    t = home + temp_dir
    tt = home + temp_dir + temp_dir2

    if os.path.isdir(t):
        pass
    else:
        os.mkdir(t)

    if os.path.isdir(tt):
        pass
    else:
        os.mkdir(tt)


def get_commands():
    global path
    global path2
    global SHOW
    global USER_AGENT_PATH
    global VERBOSE

    parser = argparse.ArgumentParser(version=__version__, description="a test server socket cli program")
    parser.add_argument('-i', '--input', action="store", help='path to text file with list of url to test', required=True)
    parser.add_argument('-o', '--output', action="store", help='path to text file to save results')
    parser.add_argument('-s', '--show', action="store_true", help='shows results at the end')
    parser.add_argument('-ver', '--verbose', action="store_true", help='Verbose ')##
    parser.add_argument('-u', '--user', action="store", help='change user agent ', required=True)


    my_Arg = parser.parse_args()

    if my_Arg.input:
        path2 = my_Arg.input

    if my_Arg.output:
        path = my_Arg.output

    if my_Arg.show:
        SHOW = True

    if my_Arg.user:
        USER_AGENT_PATH = my_Arg.user

    if my_Arg.verbose:
        VERBOSE = True

if __name__ == '__main__':
    main()