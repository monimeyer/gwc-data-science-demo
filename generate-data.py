import math
import random
import majorcities


class XoomData(object):
    header = ['transaction_id', 'payment_type', 'disbursement_type', 'recipient_country', 'send_amount', 'application', 'sender_device_latitude', 'sender_device_longitude', 'fraud_type']

    payment_types = ['credit card', 'ach']#, 'paypal wallet']
    disbursement_types = ['bank deposit', 'cash pickup', 'cash delivery', 'bill payment']#, 'mobile reload']
    recipient_countries = ['AT', 'CL', 'EE', 'EG', 'JM', 'LV', 'MX', 'NZ', 'TT', 'BE', 'CY', 'SI', 'TN', 'UY', 'ZA', 'AU', 'BG', 'MA', 'MT', 'NO', 'VN', 'BO', 'CA', 'CR', 'LK', 'PK', 'CZ', 'NP', 'PA', 'SV', 'FI', 'HR', 'ID', 'IT', 'BR', 'DK', 'GB', 'NI', 'CN', 'EC', 'IN', 'PT', 'DO', 'GR', 'KE', 'RO', 'AR', 'HK', 'PL', 'CO', 'HU', 'SG', 'GH', 'LU', 'NL', 'HN', 'LT', 'SE', 'GT', 'HT', 'PE', 'FR', 'NG', 'PH', 'CH', 'ES', 'DE', 'PY', 'SK', 'JP', 'BD', 'GY', 'IE']
    applications = ['web', 'mobile app']
    fraud_types = ['unauthorized payment source', 'not sufficient funds', 'account take over']

    def __init__(self, cg):
        self.initalized = True
        self.circle_generator = cg

    def randList(self, li):
        return li[random.randrange(0, len(li))]

    def weightedRandList(self, li, weights):
        norm_weights = map(lambda x: float(x) / sum(weights), weights)
        norm_weights = [sum(norm_weights[:idx]) for idx in range(1, len(norm_weights) + 1)]
        randn = random.uniform(0, 1)
        for idx, w in enumerate(norm_weights):
            if randn < w:
                return li[idx]

    def randCurrency(self, smin=1.0, smax=25000.0):
        return round(random.uniform(smin, smax), 2)

    def randLatLong(self, li):
        lat, lng = self.randList(li)
        return (lat, lng)

    def weightedRandLatLong(self, li):
        lat, lng = self.weightedRandList(li, [random.randrange(0, 150) for latlong in li])
        return (lat, lng)

    def goodTxn(self):
        rand_lat, rand_long = self.randLatLong(majorcities.lat_long)
        randn = random.randrange(0, 1000)
        fraud_type = 'None' if randn < 990 else self.weightedRandList(self.fraud_types, [5, 2, 4])
        return [self.weightedRandList(self.payment_types, [16, 21]),
                self.weightedRandList(self.disbursement_types, [19, 13, 5, 9]),
                self.weightedRandList(self.recipient_countries, [random.randrange(0, 30) for country in self.recipient_countries]),
                self.randCurrency(),
                self.weightedRandList(self.applications, [5, 8]),
                rand_lat,
                rand_long,
                fraud_type]

    def fraudTrendMap1(self):
        fraud_lat, fraud_long = self.circle_generator.next()
        return [self.weightedRandList(self.payment_types, [23, 19]),
                self.disbursement_types[1],
                self.recipient_countries[42],
                self.randCurrency(100, 1000),
                self.weightedRandList(self.applications, [11, 4]),
                fraud_lat,
                fraud_long,
                self.weightedRandList(self.fraud_types, [5, 2, 13]),
                ]

    def fraudTrendMap2(self):
        fraud_lat, fraud_long = self.weightedRandLatLong(majorcities.lat_long[40:50])
        return [self.weightedRandList(self.payment_types, [21, 16]),
                self.disbursement_types[1],
                self.recipient_countries[6],
                self.randCurrency(1000, 10000),
                self.weightedRandList(self.applications, [15, 13]),
                fraud_lat,
                fraud_long,
                self.weightedRandList(self.fraud_types, [5, 1, 10]),
                ]

    def fraudTrendUPS(self):
        fraud_lat, fraud_long = self.weightedRandLatLong(majorcities.lat_long)
        return[self.payment_types[0],
               self.disbursement_types[3],
               self.weightedRandList(self.recipient_countries, [random.randrange(0, 20) for country in self.recipient_countries]),
               self.randCurrency(1, 100),
               self.applications[0],
               fraud_lat,
               fraud_long,
               self.fraud_types[0],
               ]


def genCircle(midpoint=(0.0, 0.0), radius=1.0, step_in_radians=math.pi / 180):
    '''
    (x - h)^2 + (y - k)^2 = r^2
    '''
    x = midpoint[0] + radius
    y = midpoint[1]
    theta = 0
    while True:
        yield (x, y)
        x = midpoint[0] + math.cos(theta) * radius
        y = midpoint[1] + math.sin(theta) * radius
        theta += step_in_radians + random.uniform(-0.001, 0.001)


def main():
    sample_number = 100000
    with open('gwc-risk-dataset.csv', 'w') as of:
        of.write(','.join(xoom_data.header) + '\n')
        for i in range(1, sample_number + 1):
            randn = random.randrange(0, 10000)
            if randn >= 9999:
                of.write(','.join([str(x) for x in [i] + xoom_data.fraudTrendMap1()]) + '\n')
            elif randn >= 9000:
                of.write(','.join([str(x) for x in [i] + xoom_data.fraudTrendMap2()]) + '\n')
            elif randn >= 8000:
                of.write(','.join([str(x) for x in [i] + xoom_data.fraudTrendUPS()]) + '\n')
            else:
                of.write(','.join([str(x) for x in [i] + xoom_data.goodTxn()]) + '\n')
            if i % 1000 == 0:
                print i

    pass

if __name__ == '__main__':
    bemidji_circle_gen = genCircle(midpoint=(47.4925977, -94.8841771), radius=0.25, step_in_radians=math.pi / 16)
    xoom_data = XoomData(bemidji_circle_gen)
    main()
