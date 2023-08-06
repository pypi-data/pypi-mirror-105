import os
import geoip2.database
import geoip2.errors
import logging

logger = logging.getLogger(__name__)


class GeoLite:
    path = os.path.dirname(os.path.abspath(__file__))
    reader_info = geoip2.database.Reader(path + '/GeoLite2-City.mmdb', locales='zh-CN')
    reader_isp = geoip2.database.Reader(path + '/GeoLite2-ASN.mmdb', locales='zh-CN')

    @classmethod
    def get_info_by_ip(cls, ip):
        info = {
            "city": "",  # 城市
            "continent": "",  # 大洲
            "country": "",  # 国家
            # "location": {
            "lat": "",
            "lon": "",
            # },
            # "registered_country": "",
            "subdivisions": "",
            "isp": "",
            'asn': ""
        }
        try:
            res = cls.reader_info.city(ip)
            info['asn'] = cls.get_asn_by_ip(ip)
            info['isp'] = cls.get_isp_by_ip(ip)
            info['lat'] = res.location.latitude
            info['lon'] = res.location.longitude
            info['continent'] = res.continent.names[res._locales] if res.continent.names else ''
            info['country'] = res.country.names[res._locales] if res.country.names else ''
            info['city'] = res.city.names[res._locales] if res.city.names and 'zh-CN' in res.city.names else ''
            if res.subdivisions:
                try:
                    info['subdivisions'] = res.subdivisions[0].names[res._locales]
                except:
                    info['subdivisions'] = res.subdivisions[0].names['en']
            else:
                info['subdivisions'] = ''

            info['addr'] = info['country']
            if info['subdivisions']:
                info['addr'] += '-' + info['subdivisions']
            if info['city'] and info['city'] != info['subdivisions']:
                info['addr'] += '-' + info['city']

            if ip == '127.0.0.1':
                info['addr'] = '本机地址'
            elif ip.startswith('127.'):
                info['addr'] = '局域网'
            elif ip.startswith('192.168.'):
                info['addr'] = '局域网'
            return info
        except geoip2.errors.AddressNotFoundError as e:
            if ip == '127.0.0.1':
                info['addr'] = '本机地址'
            elif ip.startswith('127.'):
                info['addr'] = '局域网'
            elif ip.startswith('192.168.'):
                info['addr'] = '局域网'
            else:
                info['addr'] = '未知'
        except Exception as e:
            logger.warning(e, exc_info=True)
            if ip == '127.0.0.1':
                info['addr'] = '本机地址'
            elif ip.startswith('127.'):
                info['addr'] = '局域网'
            elif ip.startswith('192.168.'):
                info['addr'] = '局域网'
            else:
                info['addr'] = '未知'
        return info

    @classmethod
    def get_isp_by_ip(cls, ip):
        return cls.reader_isp.asn(ip).autonomous_system_organization

    @classmethod
    def get_asn_by_ip(cls, ip):
        return cls.reader_isp.asn(ip).autonomous_system_number


if __name__ == "__main__":
    GeoLite.get_info_by_ip("95.210.119.104")
