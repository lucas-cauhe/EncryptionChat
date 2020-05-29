from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import  hashes
from cryptography.hazmat.backends import default_backend
import json
class genKeys:

    def __init__(self, privateKey, publicKey):
        self.privateKey = privateKey
        self.publicKey = publicKey

    def publicKey_gen(self):

        publicBytes = self.publicKey.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return publicBytes


    def privateKey_gen(self):

        privateBytes = self.privateKey.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        return privateBytes

    def privateEnc(self):
        return self.privateKey_gen().decode('latin-1')
    def publicEnc(self):
        return self.publicKey_gen().decode('latin-1')
    def private_load_enc(self):
        return str(Ed25519PrivateKey.from_private_bytes(self.privateKey_gen()))
    def public_load_enc(self):
        return str(Ed25519PublicKey.from_public_bytes(self.publicKey_gen()))

    def certificates(self):
        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Computing Fun"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"http://comp-fun.netlify.app"),
        ])).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(u"http://comp-fun.netlify.app")
            ]),
            critical=False,
        ).sign(self.privateKey_gen(), hashes.SHA256(), default_backend())
        return csr


