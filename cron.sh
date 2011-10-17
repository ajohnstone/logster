GRAPHITE_HOST="graphite.example.com:2003";

sanitized_name_host=$(echo `hostname` | sed 's/[.]/_/g;');
/usr/sbin/logster -D --metric-prefix="servers.${sanitized_name_host}.apache.error_log" --output=graphite --graphite-host=$GRAPHITE_HOST ApacheErrorLogster /var/log/apache2/error.log

for i in $(ls /var/www/vhosts/); do
    sanitized_name=$(echo $i | sed 's/[.]/_/g;');
    /usr/sbin/logster -D --metric-prefix="servers.${sanitized_name_host}.project.${sanitized_name}.apache.error_log" --output=graphite --graphite-host=$GRAPHITE_HOST ApacheErrorLogster /var/www/vhosts/$i/statistics/logs/error.log
done;

