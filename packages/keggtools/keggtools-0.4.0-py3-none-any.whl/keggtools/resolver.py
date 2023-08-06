""" Resolve requests to KEGG data Api """

import logging
from .utils import parse_tsv, request
from .storage import KEGGDataStorage
from .models import KEGGPathway


class KEGGPathwayResolver:
    """
    KEGGPathwayResolver
    Request interface for KEGG API endpoint
    """
    def __init__(self, org: str):
        """
        Need <org> 3 letter code for organism
        :param org: str
        """

        if type(org) != str:
            logging.error(f"Expect type str. Got type {type(org).__name__}")
            raise TypeError("Expect type str for organism.")

        self.organism = org


    @staticmethod
    def request(url: str):
        """
        GET request to given Url
        :param url: str
        :return: byte
        """

        return request(url=url)


    def get_pathway_list(self):
        """
        Request list of pathways linked to organism. {<pathway-id>: <name>}
        :return: dict
        """

        # path:mmu00010	Glycolysis / Gluconeogenesis - Mus musculus (mouse)
        # path:<org><code>\t<name> - <org>

        # Request list of pathways from API

        store = KEGGDataStorage()
        if store.pathway_list_exist(org=self.organism):
            # return pathway list dump
            logging.debug(f"Found pathway list for organism {self.organism} in cache.")
            data = store.load_dump(filename="pathway_{ORG}.dump".format(ORG=self.organism))
            return data

        else:
            # request pathway list
            logging.debug(f"Not found pathway list for organism {self.organism} in cache. Requesting from API")
            data = parse_tsv(KEGGPathwayResolver.request(url="http://rest.kegg.jp/list/pathway/{ORG}".format(ORG=self.organism)))
            pathways = {}
            for line in data:
                if len(line) == 2 and line[0] != "":
                    pathways[line[0].split(":")[1].strip(self.organism)] = line[1].split(" - ")[0]

            logging.debug("Loading list of {N} pathways for organism {ORG}".format(N=len(pathways.keys()), ORG=self.organism))

            # save dump
            store.save_dump(filename="pathway_{ORG}.dump".format(ORG=self.organism), data=pathways)

            # return pathway list
            return pathways


    @staticmethod
    def build_url(org: str, code: str):
        """
        Build path to KGML File at KEGG API endpint
        :param org: str
        :param code: str
        :return: str
        """
        return "http://rest.kegg.jp/get/{ORG}{CODE}/kgml".format(ORG=org, CODE=code)

    def get_pathway(self, code: str):
        """
        Request pathway by code
        :param code: str
        :return: KEGGPathway
        """
        store = KEGGDataStorage()
        if store.pathway_file_exist(org=self.organism, code=code):
            # load from file
            data = store.load(filename="{ORG}_path{CODE}.kgml".format(ORG=self.organism, CODE=code))
            logging.debug("Load pathway path:{ORG}{CODE} from file".format(ORG=self.organism, CODE=code))
        else:
            # request pathway and store
            data = KEGGPathwayResolver.request(KEGGPathwayResolver.build_url(org=self.organism, code=code))
            store.save(filename="{ORG}_path{CODE}.kgml".format(ORG=self.organism, CODE=code), data=data)
            logging.debug("Download pathway path:{ORG}{CODE} from rest.kegg.jp".format(ORG=self.organism, CODE=code))
        return KEGGPathway.parse(data)

    def link_pathways(self, geneid: str):
        """
        Return all pathways linked to gene-id
        :param geneid: str
        :return: list
        """
        data = parse_tsv(KEGGPathwayResolver.request("http://rest.kegg.jp/link/pathway/{ORG}:{ID}".format(ORG=self.organism, ID=geneid)))
        result = []
        for item in data:
            if len(item) == 2 and item[0] != "":
                result.append(item[1])
        return result

    def download_pathways(self, pathways: list):
        """
        Download all pathways from list of pathway id's.
        :param pathways:
        :return: NoneType
        """
        downloads = 0
        for code in pathways:
            if not KEGGDataStorage.pathway_file_exist(org=self.organism, code=code):
                url = KEGGPathwayResolver.build_url(org=self.organism, code=code)
                logging.debug("Requesting path:{ORG}{CODE} {URL}...".format(URL=url, ORG=self.organism, CODE=code))
                KEGGDataStorage.save(filename="{ORG}_path{CODE}.kgml".format(ORG=self.organism, CODE=code),
                                     data=KEGGPathwayResolver.request(url))
                downloads += 1
        logging.debug("Download {N} pathway KGML files from KEGG".format(N=downloads))
        return None

    @staticmethod
    def get_components():
        filename = "compound.dump"
        if not KEGGDataStorage.exist(filename=filename):
            url = "http://rest.kegg.jp/list/compound/"
            logging.debug("Requesting components {URL}...".format(URL=url))
            result = {}
            for items in parse_tsv(KEGGPathwayResolver.request(url=url)):
                if len(items) >= 2 and items[0] != "":
                    result[items[0].split(":")[1]] = items[1].split(";")[0]
            KEGGDataStorage.save_dump(filename=filename, data=result)
            return result
        else:
            return KEGGDataStorage.load_dump(filename=filename)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info(KEGGPathwayResolver.get_components())

