# docker run --rm -it -p 445:445 -p 139:139 -v $PWD:/media/storage pdxjohnny/samba

FROM alpine:3.3

RUN apk --no-cache add samba samba-common-tools

COPY smb.conf /etc/samba/smb.conf

CMD ["/usr/sbin/smbd", "-i"]
