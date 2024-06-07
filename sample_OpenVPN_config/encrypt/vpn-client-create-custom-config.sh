#!/bin/sh
my_name="${0##*/}"

help() {
	cat <<_EOF_
${my_name}: generate a vpn client.conf file

Options:

    -h, --help
        Print this help.

    -d DEV, --dev DEV
        set TUN/TAP virtual network device (tun, tap).

    -r REMOTE, --remote REMOTE
        set remote.

    -P PORT, --port PORT
        set port.

    -p PROTO, --proto PROTO
        set proto (tcp, udp).

    -C CA_CERT, --ca_cert CA_CERT
        set CA certificate encoded with DER or PEM
        (i.e. /etc/ssl/certs/ca.pem).

    -c CLIENT_CERT, --client_cert CLIENT_CERT
        set user certificate encoded with DER or PEM
        (i.e. /etc/ssl/certs/client.pem).

    -k PRIVATE_KEY, --private_key PRIVATE_KEY
        set private key encoded with DER or PEM
        (i.e. /etc/ssl/certs/client.key).

    -K PRIVATE_KEY_PASSWD, --private_key_passwd PRIVATE_KEY_PASSWD
        set private key password.

    -t TLS_CRYPT_KEY, --tls_crypt TLS_CRYPT_KEY
        set tls crypt key (OpenVPN Static key V1)
        (i.e. /etc/ssl/certs/ta.key).

    -e CIPHER, --cipher CIPHER
        set cipher.
        The following ciphers and cipher modes are available for use with OpenVPN.
        Using a CBC or GCM mode is recommended.
        In static key mode only CBC mode is allowed.

        AES-128-CBC  (128 bit key, 128 bit block)
        AES-128-CFB  (128 bit key, 128 bit block, TLS client/server mode only)
        AES-128-CFB1  (128 bit key, 128 bit block, TLS client/server mode only)
        AES-128-CFB8  (128 bit key, 128 bit block, TLS client/server mode only)
        AES-128-GCM  (128 bit key, 128 bit block, TLS client/server mode only)
        AES-128-OFB  (128 bit key, 128 bit block, TLS client/server mode only)
        AES-192-CBC  (192 bit key, 128 bit block)
        AES-192-CFB  (192 bit key, 128 bit block, TLS client/server mode only)
        AES-192-CFB1  (192 bit key, 128 bit block, TLS client/server mode only)
        AES-192-CFB8  (192 bit key, 128 bit block, TLS client/server mode only)
        AES-192-GCM  (192 bit key, 128 bit block, TLS client/server mode only)
        AES-192-OFB  (192 bit key, 128 bit block, TLS client/server mode only)
        AES-256-CBC  (256 bit key, 128 bit block)
        AES-256-CFB  (256 bit key, 128 bit block, TLS client/server mode only)
        AES-256-CFB1  (256 bit key, 128 bit block, TLS client/server mode only)
        AES-256-CFB8  (256 bit key, 128 bit block, TLS client/server mode only)
        AES-256-GCM  (256 bit key, 128 bit block, TLS client/server mode only)
        AES-256-OFB  (256 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-128-CBC  (128 bit key, 128 bit block)
        CAMELLIA-128-CFB  (128 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-128-CFB1  (128 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-128-CFB8  (128 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-128-OFB  (128 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-192-CBC  (192 bit key, 128 bit block)
        CAMELLIA-192-CFB  (192 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-192-CFB1  (192 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-192-CFB8  (192 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-192-OFB  (192 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-256-CBC  (256 bit key, 128 bit block)
        CAMELLIA-256-CFB  (256 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-256-CFB1  (256 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-256-CFB8  (256 bit key, 128 bit block, TLS client/server mode only)
        CAMELLIA-256-OFB  (256 bit key, 128 bit block, TLS client/server mode only)
        SEED-CBC  (128 bit key, 128 bit block)
        SEED-CFB  (128 bit key, 128 bit block, TLS client/server mode only)
        SEED-OFB  (128 bit key, 128 bit block, TLS client/server mode only)

        The following ciphers have a block size of less than 128 bits,
        and are therefore deprecated.  Do not use unless you have to.

        BF-CBC  (128 bit key by default, 64 bit block)
        BF-CFB  (128 bit key by default, 64 bit block, TLS client/server mode only)
        BF-OFB  (128 bit key by default, 64 bit block, TLS client/server mode only)
        CAST5-CBC  (128 bit key by default, 64 bit block)
        CAST5-CFB  (128 bit key by default, 64 bit block, TLS client/server mode only)
        CAST5-OFB  (128 bit key by default, 64 bit block, TLS client/server mode only)
        DES-CBC  (64 bit key, 64 bit block)
        DES-CFB  (64 bit key, 64 bit block, TLS client/server mode only)
        DES-CFB1  (64 bit key, 64 bit block, TLS client/server mode only)
        DES-CFB8  (64 bit key, 64 bit block, TLS client/server mode only)
        DES-EDE-CBC  (128 bit key, 64 bit block)
        DES-EDE-CFB  (128 bit key, 64 bit block, TLS client/server mode only)
        DES-EDE-OFB  (128 bit key, 64 bit block, TLS client/server mode only)
        DES-EDE3-CBC  (192 bit key, 64 bit block)
        DES-EDE3-CFB  (192 bit key, 64 bit block, TLS client/server mode only)
        DES-EDE3-CFB1  (192 bit key, 64 bit block, TLS client/server mode only)
        DES-EDE3-CFB8  (192 bit key, 64 bit block, TLS client/server mode only)
        DES-EDE3-OFB  (192 bit key, 64 bit block, TLS client/server mode only)
        DES-OFB  (64 bit key, 64 bit block, TLS client/server mode only)
        DESX-CBC  (192 bit key, 64 bit block)
        RC2-40-CBC  (40 bit key by default, 64 bit block)
        RC2-64-CBC  (64 bit key by default, 64 bit block)
        RC2-CBC  (128 bit key by default, 64 bit block)
        RC2-CFB  (128 bit key by default, 64 bit block, TLS client/server mode only)
        RC2-OFB  (128 bit key by default, 64 bit block, TLS client/server mode only)

        Set --cipher=none to disable encryption.

    -a AUTH, --auth AUTH
        set auth.
        The following message digests are available for use with OpenVPN.
        A message digest is used in conjunction with the HMAC function,
        to authenticate received packets.

        MD5 128 bit digest size
        RSA-MD5 128 bit digest size
        SHA 160 bit digest size
        RSA-SHA 160 bit digest size
        SHA1 160 bit digest size
        RSA-SHA1 160 bit digest size
        DSA-SHA 160 bit digest size
        DSA-SHA1-old 160 bit digest size
        DSA-SHA1 160 bit digest size
        RSA-SHA1-2 160 bit digest size
        DSA 160 bit digest size
        RIPEMD160 160 bit digest size
        RSA-RIPEMD160 160 bit digest size
        MD4 128 bit digest size
        RSA-MD4 128 bit digest size
        ecdsa-with-SHA1 160 bit digest size
        RSA-SHA256 256 bit digest size
        RSA-SHA384 384 bit digest size
        RSA-SHA512 512 bit digest size
        RSA-SHA224 224 bit digest size
        SHA256 256 bit digest size
        SHA384 384 bit digest size
        SHA512 512 bit digest size
        SHA224 224 bit digest size
        whirlpool 512 bit digest size

        Set --auth=none to disable authentication.

    -z FILE, --authuserpass FILE
        Authenticate with server using username/password.
        FILE is a file containing username/password on 2 lines.

    -u hostname port, --http_proxy hostname port
        set proxy hostname and port
_EOF_
}

check_dev() {
	if [ "${dev}" != "tun" ] && [ "${dev}" != "tap" ]; then
		printf "error: no dev specified\n" >&2; exit 1
	fi
}

check_remote() {
	if [ -z "${remote}" ]; then
		printf "error: no remote specified\n" >&2; exit 1
	fi
}

check_port() {
	if [ -z "${port}" ]; then
		printf "error: no port specified\n" >&2; exit 1
	fi
}

check_proto() {
	if [ "${proto}" != "tcp" ] && [ "${proto}" != "udp" ]; then
		printf "error: no proto specified\n" >&2; exit 1
	fi
}

check_ca_cert() {
	if [ ! -z "${ca_cert}" ]; then
		ca_cert_data="$(openssl x509 -in "${ca_cert}" 2>/dev/null)"
		if [ $? -ne 0 ]; then
			printf "error: CA certificate not valid\n" >&2; exit 1
		fi
	fi
}

check_client_cert() {
	if [ ! -z "${client_cert}" ]; then
		client_cert_data="$(openssl x509 -in "${client_cert}" 2>/dev/null)"
		if [ $? -ne 0 ]; then
			printf "error: user certificate not valid\n" >&2; exit 1
		fi
	fi
}

check_private_key() {
	if [ ! -z "${private_key}" ]; then
		# hack: private key password must be not empty to avoid "hang" whether private key is encrypted
		[ ! -z "${private_key_passwd}" ] || private_key_passwd="null"
		private_key_data="$(openssl pkcs8 -topk8 -nocrypt -in "${private_key}" -passin pass:"${private_key_passwd}" 2>/dev/null)"
		if [ $? -ne 0 ]; then
			printf "error: private key not valid\n" >&2; exit 1
		fi
	fi
}

check_tls_crypt() {
	if [ ! -z "${tls_crypt}" ]; then
		tls_crypt_data="$(sed -n '/BEGIN OpenVPN Static key V1/,/END OpenVPN Static key V1/p' ${tls_crypt})"
		if [ $? -ne 0 ] || [ -z "${tls_crypt_data}" ]; then
			printf "error: tls crypt key not valid\n" >&2; exit 1
		fi
	fi
}

check_cipher() {
	case "${cipher}" in
	AES-128-CFB|AES-128-CFB1|AES-128-CFB8|AES-128-GCM|AES-128-OFB| \
	AES-192-CFB|AES-192-CFB1|AES-192-CFB8|AES-192-GCM|AES-192-OFB| \
	AES-256-CFB|AES-256-CFB1|AES-256-CFB8|AES-256-GCM|AES-256-OFB| \
	CAMELLIA-128-CFB|CAMELLIA-128-CFB1|CAMELLIA-128-CFB8|CAMELLIA-128-OFB| \
	CAMELLIA-192-CFB|CAMELLIA-192-CFB1|CAMELLIA-192-CFB8|CAMELLIA-192-OFB| \
	CAMELLIA-256-CFB|CAMELLIA-256-CFB1|CAMELLIA-256-CFB8|CAMELLIA-256-OFB| \
	SEED-CFB|SEED-OFB| \
	BF-CFB|BF-OFB| \
	CAST5-CFB|CAST5-OFB| \
	DES-CFB|DES-CFB1|DES-CFB8| \
	DES-EDE-CFB|DES-EDE-OFB| \
	DES-EDE3-CFB|DES-EDE3-CFB1|DES-EDE3-CFB8|DES-EDE3-OFB|DES-OFB| \
	RC2-CFB|RC2-OFB)
		;;
	AES-128-CBC|AES-192-CBC|AES-256-CBC| \
	CAMELLIA-128-CBC|CAMELLIA-192-CBC|CAMELLIA-256-CBC| \
	SEED-CBC| \
	BF-CBC| \
	CAST5-CBC| \
	DES-CBC| \
	DES-EDE-CBC|DES-EDE3-CBC|DESX-CBC| \
	RC2-40-CBC|RC2-64-CBC|RC2-CBC| \
	none)
		;;
	*)
		printf "error: cipher not valid\n" >&2; exit 1
	esac
}

check_auth() {
	case "${auth}" in
	MD5| \
	RSA-MD5| \
	SHA| \
	RSA-SHA| \
	SHA1| \
	RSA-SHA1| \
	DSA-SHA| \
	DSA-SHA1-old| \
	DSA-SHA1| \
	RSA-SHA1-2| \
	DSA| \
	RIPEMD160| \
	RSA-RIPEMD160| \
	MD4| \
	RSA-MD4| \
	ecdsa-with-SHA1| \
	RSA-SHA256| \
	RSA-SHA384| \
	RSA-SHA512| \
	RSA-SHA224| \
	SHA256| \
	SHA384| \
	SHA512| \
	SHA224| \
	whirlpool| \
	none)
		;;
	*)
		printf "error: auth not valid\n" >&2; exit 1
	esac
}

main() {
	local o O opts
	local dev remote port proto ca_cert client_cert private_key private_key_passwd tls_crypt cipher auth authuserpass
	local verbose

	verbose=0
	o='hvd:r:P:p:C:c:k:K:t:e:a:z:u:'
	O='help,verbose,dev:,remote:,port:,proto:,ca_cert:,client_cert:,private_key:,private_key_passwd:,tls_crypt:,cipher:,auth:,authuserpass:,http_proxy:'
	opts="$(getopt -n "${my_name}" -o "${o}" -l "${O}" -- "${@}")"
	[ $? -eq 0 ] || exit 1
	eval set -- "${opts}"

	while true
	do
	case "${1}" in
	-h|--help)
		help
		exit 0
		;;
	-d|--dev)
		shift
		dev="${1}"
		;;
	-r|--remote)
		shift
		remote="${1}"
		;;
	-P|--port)
		shift
		port="${1}"
		;;
	-p|--proto)
		shift
		proto="${1}"
		;;
	-C|--ca_cert)
		shift
		ca_cert="${1}"
		;;
	-c|--client_cert)
		shift
		client_cert="${1}"
		;;
	-k|--private_key)
		shift
		private_key="${1}"
		;;
	-K|--private_key_passwd)
		shift
		private_key_passwd="${1}"
		;;
	-t|--tls_crypt)
		shift
		tls_crypt="${1}"
		;;
	-e|--cipher)
		shift
		cipher="${1}"
		;;
	-a|--auth)
		shift
		auth="${1}"
		;;
	-z|--authuserpass)
		shift
		authuserpass="${1}"
		;;
	-u|--http_proxy)
		shift
		http_proxy="${1}"
		;;
	-v|--verbose)
		verbose=1
		set -xv  # Set xtrace and verbose mode.
		;;
	--)
		shift
		break;;
	esac
	shift
	done

	check_dev
	check_remote
	check_proto
	check_port
	check_ca_cert
	check_client_cert
	check_private_key
	check_tls_crypt
	check_cipher
	check_auth

	cat <<_EOF_
client
dev openvpn-client
dev-type ${dev}
proto ${proto}

remote ${remote} ${port}
resolv-retry infinite
nobind

persist-key

txqueuelen 1000
resolv-retry infinite
connect-retry-max unlimited
connect-retry 1 30
connect-timeout 5
push-peer-info
reneg-sec 0

remote-cert-tls server
auth-nocache
auth ${auth}
cipher ${cipher}

mute-replay-warnings

verb 3
_EOF_
[ -z "${http_proxy}" ] || (echo "http-proxy ${http_proxy}")
[ -z "${authuserpass}" ] || (echo "auth-user-pass ${authuserpass}")
[ -z "${ca_cert}" ] || (echo "<ca>";echo "${ca_cert_data}";echo "</ca>")
[ -z "${client_cert}" ] || (echo "<cert>";echo "${client_cert_data}";echo "</cert>")
[ -z "${private_key}" ] || (echo "<key>";echo "${private_key_data}";echo "</key>")
[ -z "${tls_crypt}" ] || (echo "<tls-crypt>";echo "${tls_crypt_data}";echo "</tls-crypt>")
}

main "${@}"
