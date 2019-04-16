import urllib.request
import json
from shapely.geometry import Polygon, Point
import json
import dml
import prov.model
import datetime
import csv
import codecs
import uuid
from scipy.stats import pearsonr

class statistics(dml.Algorithm):
    contributor = 'gasparde_ljmcgann_tlux'
    reads = [contributor + ".CensusTractShape", contributor + ".CensusTractHealth",
             contributor + ".Neighborhoods", contributor + ".ParcelAssessments",
             contributor + ".ParcelGeo"]
    writes = []

    @staticmethod
    def execute(trial = False):


        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate(statistics.contributor, statistics.contributor)
        parcels = repo[statistics.contributor + ".ParcelsCombined"]
        neighborhoods = list(repo[statistics.contributor + ".Neighborhoods"].find())

        repo.dropCollection(statistics.contributor + ".Statistics")
        repo.createCollection(statistics.contributor + ".Statistics")
        for i in range(len(neighborhoods)):
            name = neighborhoods[i]["properties"]["Name"]
            print(name)
            data = list(parcels.find({"Neighborhood":name}))

            for category in ["obesity", "asthma", "low_phys"]:
                x = []
                y = []
                for i in range(len(data)):
                    print(data[i])
                    y.append(float(data[i][category]))
                    x.append(float(data[i]["min_distance_km"]))

                corr = pearsonr(x,y)
            repo[statistics.contributor + ".Statistics"].insert_one({"Neighborhood": name , "health_category": category,
                                                                     "pearsonr": corr})

    @staticmethod
    def provenance():
        return 0

statistics.execute()