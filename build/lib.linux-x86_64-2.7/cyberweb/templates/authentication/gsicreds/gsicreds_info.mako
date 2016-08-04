<%inherit file="./gsicreds.layout.mako"/>

<%def name="headtags()">
</%def>


<%def name="col2main()">

<h2>CREATE:  GSI Credential Management for CyberWeb User: ${c.user}</h2>
<p>
<p> status: ${c.status}
<p>
<h3>DUMP CREDENTIAL INFO:  using command:</h3>
 <blockquote>
openssl x509 -in /tmp/x509up_u501 -noout -text
 </blockquote>
${c.gsidump}
<h3>EXAMPLE OF CREDENTIAL INFO</h3>
<blockquote>
<pre>
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 1624757 (0x18cab5)
        Signature Algorithm: sha1WithRSAEncryption
        Issuer: C=US, O=National Center for Supercomputing Applications, OU=Certificate Authorities, CN=MyProxy
        Validity
            Not Before: Mar 30 18:28:30 2012 GMT
            Not After : Mar 31 06:33:30 2012 GMT
        Subject: C=US, O=National Center for Supercomputing Applications, CN=Mary Thomas
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (1024 bit)
                Modulus:
                    00:b5:1e:00:a4:e5:16:da:de:d0:6d:c5:eb:e4:5c:
                    45:13:a7:94:d3:5f:3f:90:7a:c3:db:89:0b:b7:2d:
                    5a:d8:7b:d5:4d:e9:57:b5:43:d6:4f:a7:c3:93:f6:
                    f7:87:f1:0c:71:d5:7d:1b:3a:80:02:9c:cc:d1:c5:
                    aa:89:3e:32:ab:e2:53:8a:78:18:ee:7b:d1:0c:e2:
                    fe:fd:ba:4b:36:9a:bc:53:05:0c:c6:f4:bb:6f:09:
                    e8:60:ae:68:ad:8c:3c:31:54:14:6b:02:d0:1d:95:
                    01:f0:ba:c3:86:42:03:00:72:25:58:c1:68:28:cd:
                    7c:0e:9b:09:4b:ca:ce:01:19
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Key Usage: critical
                Digital Signature, Key Encipherment, Data Encipherment
            X509v3 Subject Key Identifier: 
                23:82:99:81:92:2D:B9:DB:83:53:6E:04:7A:8F:C4:D5:56:1D:B1:92
            X509v3 Authority Key Identifier: 
                keyid:D7:FC:A5:02:76:3A:F6:13:FA:2B:A1:E0:E6:50:35:C7:23:C7:7B:51

            X509v3 Basic Constraints: critical
                CA:FALSE
            X509v3 Certificate Policies: 
                Policy: 1.3.6.1.4.1.4670.100.2.5
                Policy: 1.2.840.113612.5.2.2.3
                Policy: 1.2.840.113612.5.2.3.2.1

            X509v3 CRL Distribution Points: 

                Full Name:
                  URI:http://ca.ncsa.uiuc.edu/f2e89fe3.crl

    Signature Algorithm: sha1WithRSAEncryption
        50:6c:f7:51:cf:2e:f6:e3:d6:61:6a:55:17:e1:f1:62:ba:c3:
        ac:7f:cc:61:d9:52:21:21:b3:fe:f3:df:86:b9:3f:94:f1:41:
        3c:0b:e4:48:66:c7:3d:80:82:7f:96:a9:24:8e:44:4a:ba:6e:
        72:53:91:26:71:13:63:e1:6c:17:73:ab:2e:72:47:62:6d:73:
        a2:65:07:63:d4:00:df:06:02:92:e7:d1:52:77:73:d6:42:ce:
        7a:f8:da:e4:67:12:af:91:6d:e4:38:78:37:ec:2e:c8:27:5d:
        43:1c:05:81:44:c0:5c:2f:64:89:08:ca:c6:ba:71:ae:d7:aa:
        7e:40:cb:12:10:26:76:8c:e6:89:be:7a:01:4b:24:a3:a6:86:
        5a:1e:33:cf:1c:0a:6c:8f:bf:53:92:3e:dc:91:8e:54:f0:6a:
        43:ee:50:b5:d3:a4:ce:ef:4d:10:5a:60:36:d4:ff:d2:8d:1b:
        a4:63:56:f5:ea:39:ca:44:6d:27:de:fe:05:e2:56:86:7a:b7:
        ab:29:07:3e:bd:e8:2e:42:e0:08:e4:00:e1:4c:28:ad:a9:3b:
        2f:8b:4f:2e:a6:a8:2c:7a:f1:76:7a:b3:bc:c9:4e:76:4a:5e:
        c2:da:c4:54:76:5f:1c:50:cb:f7:22:c3:5e:41:e8:a2:01:b1:
        43:c2:09:26


</pre>
</blockquote>
<hr>
<%
  session = request.environ['beaker.session']
  g = app_globals
%>
% for k,v,admin in g.menu.find_menu('gsicreds','index',1):
    <li class=current>IDX1  V: "${v}, K=${k}</li>
% endfor
<hr>
% for k,v,admin in g.menu.find_menu('gsicreds','index',2):
    <li class=current>IDX2  V: "${v}, K=${k}</li>
% endfor
<hr>
% for k,v,admin in g.menu.find_menu('gsicreds','index',3):
    <li class=current>IDX3  V: "${v}, K=${k}</li>
% endfor
<hr>

</%def>
