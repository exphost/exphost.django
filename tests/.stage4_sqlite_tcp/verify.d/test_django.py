def test_django_sqlite(host):
  host.ansible(
    "command",
    "yum install -y nc",
    become=True,
    check=False,
  )
  assert host.check_output(r'OUTPUT=""; SIZE=0; function add_element { OUTPUT="$OUTPUT\x$(printf "%02x" $(( ${#1} & 0xff )))\x$(printf "%02x" $(( (${#1} >> 8) & 0xff )))$1"; OUTPUT="$OUTPUT\x$(printf "%02x" $(( ${#2} & 0xff )))\x$(printf "%02x" $(( (${#2} >> 8) & 0xff )))$2"; SIZE=$(($SIZE+${#1} + ${#2} +4));}; add_element "REQUEST_METHOD" "GET"; add_element "SERVER_NAME" "localhost"; add_element "SERVER_PORT" "8001"; add_element "QUERY_STRING" ""; add_element "CONTENT_TYPE" ""; add_element "PATH_INFO" "/test/"; OUTPUT="\x00\x$(printf "%02x" $(( $SIZE & 0xff )))\x$(printf "%02x" $(( ($SIZE >> 8) & 0xff )))\x00$OUTPUT"; echo -ne $OUTPUT | nc localhost 8001').split("\n")[-1] == "Working"
