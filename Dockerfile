FROM duckietown/rpi-duckiebot-base:master18

COPY april_to_pose.sh .

CMD ["./april_to_pose.sh"]
