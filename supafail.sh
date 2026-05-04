#remediation script for copyfail vulnerability
#
# https://arstechnica.com/security/2026/04/as-the-most-severe-linux-threat-in-years-surfaces-the-world-scrambles/
# 
# USAGE:
# run as superuser

echo "install algif_aead /bin/false" > /etc/modprobe.d/disable-algif.conf
rmmod algif_aead 2>/dev/null || true

echo "WELP. Pray to your Duckies..."
echo "(  PATCH APPLIED!  )"
