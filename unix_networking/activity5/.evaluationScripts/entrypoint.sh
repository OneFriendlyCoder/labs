#!/usr/bin/env bash
set -euo pipefail

if (( EUID != 0 )); then
  echo "This script must be run as root." >&2
  exit 1
fi

if ! command -v crontab &>/dev/null; then
  apt-get update && apt-get install -y cron
fi

if command -v service &>/dev/null; then
  service cron start || service crond start || true
elif [ -x "/etc/init.d/cron" ]; then
  /etc/init.d/cron start || true
else
  cron >/dev/null 2>&1 &
  sleep 1
fi

for u in alice bob; do
  if ! id "$u" &>/dev/null; then
    useradd -m -s /bin/bash "$u"
  fi
  bashrc="/home/$u/.bashrc"
  grep -qx 'cd "$HOME"' "$bashrc" 2>/dev/null || echo 'cd "$HOME"' >> "$bashrc"
done

generate_crons() {
  local user=$1 count=$2 home crontab_tmp
  home=$([[ $user == root ]] && echo "/root" || echo "/home/$user")
  crontab_tmp=$(mktemp)
  { crontab -u "$user" -l 2>/dev/null || :; } > "$crontab_tmp"

  for i in $(seq 1 "$count"); do
    minute=$(( RANDOM % 60 ))
    hour=$(( RANDOM % 24 ))
    log="$home/cronjob_${user}_${i}.log"

    if [[ $user == root && $(( i % 2 )) -eq 0 ]]; then
      spec="$minute $hour * 1,3,5,7,9,11 2,4"
    elif [[ $user == alice && $(( i % 2 )) -eq 1 ]]; then
      spec="$minute $hour * * 1,3,5"
    elif [[ $user == bob ]]; then
      spec="$minute $hour * 2,4,6,8,10,12 0,1,3,4"
    else
      spec="$minute $hour * * *"
    fi

    touch "$log"
    chown "$user:$user" "$log" 2>/dev/null || true

    echo "$spec bash -lc 'echo \"[\$(date)] ${user}_cronjob_${i} executed\" >> $log'" >> "$crontab_tmp"
  done

  if [[ $user == root ]]; then
    echo "0 6 * * * bash -lc 'echo \"[\$(date)] routine_backup_job executed\" >> /root/cronjob_routine_backup.log'" >> "$crontab_tmp"
    touch /root/cronjob_routine_backup.log
    chown root:root /root/cronjob_routine_backup.log 2>/dev/null || true
  fi

  if [[ $user == alice ]]; then
    echo "7 6 * 7 6 bash -lc 'echo \"[\$(date)] alice_job1 executed\" >> $home/alice_job1.log'" >> "$crontab_tmp"
    touch "$home/alice_job1.log"
    chown "$user:$user" "$home/alice_job1.log" 2>/dev/null || true

    echo "6 7 * 6 6 bash -lc 'echo \"[\$(date)] alice_job2 executed\" >> $home/alice_job2.log'" >> "$crontab_tmp"
    touch "$home/alice_job2.log"
    chown "$user:$user" "$home/alice_job2.log" 2>/dev/null || true

    echo "6 7 6 7 * bash -lc 'echo \"[\$(date)] alice_job3 executed\" >> $home/alice_job3.log'" >> "$crontab_tmp"
    touch "$home/alice_job3.log"
    chown "$user:$user" "$home/alice_job3.log" 2>/dev/null || true

    echo "6 * * 7 7 bash -lc 'echo \"[\$(date)] alice_job4 executed\" >> $home/alice_job4.log'" >> "$crontab_tmp"
    touch "$home/alice_job4.log"
    chown "$user:$user" "$home/alice_job4.log" 2>/dev/null || true
  fi

  if [[ $user == bob ]]; then
      echo "12 2 1 2 * bash -lc 'echo \"[\$(date)] bob_digest executed\" >> $home/bob_digest.log'" >> "$crontab_tmp"
      touch "$home/bob_digest.log"
      chown "$user:$user" "$home/bob_digest.log" 2>/dev/null || true

      echo "3 3 15 1 * bash -lc 'echo \"[\$(date)] bob_security_scan executed\" >> $home/bob_security_scan.log'" >> "$crontab_tmp"
      touch "$home/bob_security_scan.log"
      chown "$user:$user" "$home/bob_security_scan.log" 2>/dev/null || true

      echo "25 6 5 2 * bash -lc 'echo \"[\$(date)] bob_job1 executed\" >> $home/bob_job1.log'" >> "$crontab_tmp"
      touch "$home/bob_job1.log"
      chown "$user:$user" "$home/bob_job1.log" 2>/dev/null || true

      echo "40 7 10 2 * bash -lc 'echo \"[\$(date)] bob_job2 executed\" >> $home/bob_job2.log'" >> "$crontab_tmp"
      touch "$home/bob_job2.log"
      chown "$user:$user" "$home/bob_job2.log" 2>/dev/null || true
  fi

  if [[ $user == root ]]; then
    crontab "$crontab_tmp"
  else
    crontab -u "$user" "$crontab_tmp"
  fi

  rm -f "$crontab_tmp"
}

generate_crons alice 7
generate_crons bob 6
generate_crons root 11

exec tail -f /dev/null