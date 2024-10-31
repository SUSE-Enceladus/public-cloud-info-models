from pint_models.models import (
    AmazonImagesModel,
    AlibabaImagesModel,
    GoogleImagesModel,
    MicrosoftImagesModel,
    OracleImagesModel,
    AmazonServersModel,
    GoogleServersModel,
    MicrosoftServersModel,
    MicrosoftRegionMapModel,
    VersionsModel
)


def test_amazon_images_model():
    image = AmazonImagesModel(
        state='active',
        publishedon='20241010',
        changeinfo='https://image123.info',
        name='image123',
        id='ami-123456789',
        region='us-east-1'
    )
    assert image.state == 'active'


def test_alibaba_images_model():
    image = AlibabaImagesModel(
        state='inactive',
        publishedon='20241010',
        changeinfo='https://image123.info',
        name='image123',
        id='ami-123456789',
        region='us-east-1'
    )
    assert image.state == 'inactive'


def test_google_images_model():
    image = GoogleImagesModel(
        state='deprecated',
        publishedon='20241010',
        changeinfo='https://image123.info',
        name='image123',
        project='project123',
    )
    assert image.state == 'deprecated'


def test_microsoft_images_model():
    image = MicrosoftImagesModel(
        state='active',
        publishedon='20241010',
        changeinfo='https://image123.info',
        id='123456789',
        name='image123',
        environment='PublicAzure',
        urn='suse:sles:gen1:20241010',
    )
    assert image.state == 'active'


def test_oracle_images_model():
    image = OracleImagesModel(
        state='active',
        publishedon='20241010',
        changeinfo='https://image123.info',
        id='123456789',
        name='image123',
    )
    assert image.state == 'active'


def test_amazon_servers_model():
    server = AmazonServersModel(
        ip='192.168.0.1',
        region='us-east-1',
        ipv6='2001:db8:0:0:1:0:0:1'
    )
    assert server.ipv6 == '2001:db8:0:0:1:0:0:1'


def test_google_servers_model():
    server = GoogleServersModel(
        ip='192.168.0.1',
        region='us-east1',
        ipv6='2001:db8:0:0:1:0:0:1'
    )
    assert server.ipv6 == '2001:db8:0:0:1:0:0:1'


def test_microsoft_servers_model():
    server = MicrosoftServersModel(
        ip='192.168.0.1',
        region='eastus',
        ipv6='2001:db8:0:0:1:0:0:1'
    )
    assert server.ipv6 == '2001:db8:0:0:1:0:0:1'


def test_microsoft_region_map():
    region = MicrosoftRegionMapModel(
        environment='PublicAzure',
        region='eastus',
        canonicalname='East US'
    )
    assert region.region == 'eastus'


def test_versions_model():
    version = VersionsModel(
        tablename='table1',
        version='123'
    )
    assert version.version == '123'
