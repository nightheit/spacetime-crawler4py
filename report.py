from frequencies import *

class Report:
    def __init__():
        uniquepages = set()
        longestpage = ""
        longestpagelen = 0
        mostcommonwords = []
        subdomains = dict()
        allwords = Frequencies()
    def updateuniquepages(self, page):
        self.uniquepages.add(page)
    def updatelongestpage(self):
        pass
    def updatemostcommonwords(self):
        pass
    def updatesubdomains(self, subdomain):
        if not subdomain in subdomains:
            subdomains[subdomain]=set()
        subdomains[subdomain].add(subdomain)
        
            
    def saveReport(self):
        with open("report.txt", "w") as report:
            report.write(f"Total unique pages: {len(self.unique_pages)}\n")
            report.write(f"Longest page: {self.longestpage} "
                        f"({self.longestpagelen} words)\n\n")
            report.write("Top 50 most common words:\n")
            report.write(allwords.top(50))
            lines.append("\nSubdomain counts:\n")
            for subd in sorted(subdomains):
                lines.append(f"{subd}, {len(subdomains[subd])}\n")

        