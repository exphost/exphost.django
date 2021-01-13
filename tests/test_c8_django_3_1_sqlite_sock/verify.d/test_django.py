def test_django_sqlite_sock(host):
  host.ansible(
    "command",
    "yum install -y nc",
    become=True,
    check=False,
  )
  host.run(r'OUTPUT=""; SIZE=0; function add_element { OUTPUT="$OUTPUT\x$(printf "%02x" $(( ${#1} & 0xff )))\x$(printf "%02x" $(( (${#1} >> 8) & 0xff )))$1"; OUTPUT="$OUTPUT\x$(printf "%02x" $(( ${#2} & 0xff )))\x$(printf "%02x" $(( (${#2} >> 8) & 0xff )))$2"; SIZE=$(($SIZE+${#1} + ${#2} +4));}; add_element "REQUEST_METHOD" "GET"; add_element "SERVER_NAME" "localhost"; add_element "SERVER_PORT" "0"; add_element "QUERY_STRING" ""; add_element "CONTENT_TYPE" ""; add_element "PATH_INFO" "/test/"; OUTPUT="\x00\x$(printf "%02x" $(( $SIZE & 0xff )))\x$(printf "%02x" $(( ($SIZE >> 8) & 0xff )))\x00$OUTPUT"; echo -ne $OUTPUT > /tmp/django_request.dat')

  assert host.ansible(
    "shell",
    "nc -U /run/django/django.sock < /tmp/django_request.dat",
    become=True,
    check=False,
  )['stdout'].split("\n")[-1] == 'Working'

def test_djang_extra_dirs(host):
    media = host.file("/srv/django/media")
    assert media.is_directory
    assert media.mode == 0o755
    assert media.uid == 516
    assert media.gid == 516

    static = host.file("/srv/django/static")
    assert static.is_directory
    assert static.mode == 0o755
    assert static.uid == 0
    assert static.gid == 516

    another = host.file("/srv/django/another")
    assert another.is_directory
    assert another.mode == 0o750
    assert another.uid == 516
    assert another.gid == 0

    assert host.run("stat -c '%C' /srv/django/another|cut -f3 -d:").stdout.strip() == "httpd_sys_rw_content_t"
