# docker-ubuntu-asterisk16
Ubuntu 18 + Asterisk 16 PJSIP Build + g729 and opus codec

This is a really bare container, with the bare minimum config to get asterisk running with PJSIP and extensions.conf.

Please feel free to get in touch for any custom projects or help you might need.

# Build
docker build -t asterisk .

# Run
docker run -t asterisk
