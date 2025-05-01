from frequencies import *

class Report:
    def __init__(self):
        self.uniquepages = set()
        self.longestpage = ""
        self.longestpagelen = 0
        self.mostcommonwords = []
        self.subdomains = dict()
        self.allwords = Frequencies()
    def updateuniquepages(self, page):
        self.uniquepages.add(page)
    def updatelongestpage(self,text,page):
        t = computeWordFrequencies(tokenize(text)).total()
        if t > self.longestpagelen:
            self.longestpagelen = t
            self.longestpage = page
    def updatemostcommonwords(self, text):
        freqs = computeWordFrequencies(tokenize(text))
        self.allwords = self.allwords+freqs
    def updatesubdomains(self, subdomain):
        if not subdomain in self.subdomains:
            self.subdomains[subdomain]=set()
        self.subdomains[subdomain].add(subdomain)
        
            
    def saveReport(self):
        with open("report.txt", "w") as report:
            report.write(f"Total unique pages: {len(self.uniquepages)}\n")
            report.write(f"Longest page: {self.longestpage} "
                        f"({self.longestpagelen} words)\n\n")
            report.write("Top 50 most common words:\n")
            report.write(self.allwords.top(50))
            report.write("\n\nSubdomain counts:\n")
            for subd in sorted(self.subdomains):
                report.write(f"{subd}, {len(self.subdomains[subd])}\n")

        