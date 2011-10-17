/usr/sbin/logster -D --metric-prefix="servers.`hostname`.apache.error_log" --output=graphite --graphite-host=graphite.everlution.com:2003 ApacheErrorLogster /var/log/apache2/error.log

for i in $(ls /var/www/vhosts/); do
    sanitized_name=$(echo $i | sed 's/[.]/_/g;');
    /usr/sbin/logster -D --metric-prefix="servers.`hostname`.project.${sanitized_name}.apache.error_log" --output=graphite --graphite-host=graphite.example.com:2003 ApacheErrorLogster /var/www/vhosts/$i/statistics/logs/error.log
done;

