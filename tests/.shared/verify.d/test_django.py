def test_django_sqlite(host):
  host.ansible(
    "command",
    "yum install -y nc",
    become=True,
    check=False,
  )
  assert host.check_output(r'function add_element { OUTPUT="$OUTPUT\x$(printf "%02x" $(( ${#1} & 0xff )))\x$(printf "%02x" $(( (${#1} >> 8) & 0xff )))$1"; OUTPUT="$OUTPUT\x$(printf "%02x" $(( ${#2} & 0xff )))\x$(printf "%02x" $(( (${#2} >> 8) & 0xff )))$2"; SIZE=$(($SIZE+${#1} + ${#2} +4));}; add_element "REQUEST_METHOD" "GET"; add_element "SERVER_NAME" "localhost"; add_element "SERVER_PORT" "8001"; add_element "QUERY_STRING" ""; add_element "CONTENT_TYPE" ""; add_element "PATH_INFO" "/test/"; OUTPUT="\x00\x$(printf "%02x" $(( $SIZE & 0xff )))\x$(printf "%02x" $(( ($SIZE >> 8) & 0xff )))\x00$OUTPUT"; echo -ne $OUTPUT | nc localhost 8001').split("\n")[-1] == "Working"

def test_django_sqlite_sock(host):
  host.ansible(
    "command",
    "yum install -y nc",
    become=True,
    check=False,
  )
  host.run(r'function add_element { OUTPUT="$OUTPUT\x$(printf "%02x" $(( ${#1} & 0xff )))\x$(printf "%02x" $(( (${#1} >> 8) & 0xff )))$1"; OUTPUT="$OUTPUT\x$(printf "%02x" $(( ${#2} & 0xff )))\x$(printf "%02x" $(( (${#2} >> 8) & 0xff )))$2"; SIZE=$(($SIZE+${#1} + ${#2} +4));}; add_element "REQUEST_METHOD" "GET"; add_element "SERVER_NAME" "localhost"; add_element "SERVER_PORT" "0"; add_element "QUERY_STRING" ""; add_element "CONTENT_TYPE" ""; add_element "PATH_INFO" "/test/"; OUTPUT="\x00\x$(printf "%02x" $(( $SIZE & 0xff )))\x$(printf "%02x" $(( ($SIZE >> 8) & 0xff )))\x00$OUTPUT"; echo -ne $OUTPUT > /tmp/django_sqlite_sock_request.dat')

  assert host.ansible(
    "shell",
    "nc -U /run/django_sqlite_sock/django_sqlite_sock.sock < /tmp/django_sqlite_sock_request.dat",
    become=True,
    check=False,
  )['stdout'].split("\n")[-1] == 'Working'

def test_django_mysql(host):
  host.ansible(
    "command",
    "yum install -y nc",
    become=True,
    check=False,
  )
  assert host.check_output(r'function add_element { OUTPUT="$OUTPUT\x$(printf "%02x" $(( ${#1} & 0xff )))\x$(printf "%02x" $(( (${#1} >> 8) & 0xff )))$1"; OUTPUT="$OUTPUT\x$(printf "%02x" $(( ${#2} & 0xff )))\x$(printf "%02x" $(( (${#2} >> 8) & 0xff )))$2"; SIZE=$(($SIZE+${#1} + ${#2} +4));}; add_element "REQUEST_METHOD" "GET"; add_element "SERVER_NAME" "localhost"; add_element "SERVER_PORT" "8003"; add_element "QUERY_STRING" ""; add_element "CONTENT_TYPE" ""; add_element "PATH_INFO" "/test/"; OUTPUT="\x00\x$(printf "%02x" $(( $SIZE & 0xff )))\x$(printf "%02x" $(( ($SIZE >> 8) & 0xff )))\x00$OUTPUT"; echo -ne $OUTPUT | nc localhost 8003').split("\n")[-1] == "Working"
