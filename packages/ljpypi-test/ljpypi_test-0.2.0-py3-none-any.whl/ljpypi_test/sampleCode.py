class Calculator:
    def __init__(self, par01, par02):
        self.par01, self.par02 = par01, par02
        print("This is PyPI Uploading Test Code V0.2.0")
        print(f"Input parameter is {self.par01, self.par02}")

    def add(self):
        return self.par01 + self.par02

    def substract(self):
        return self.par01 - self.par02
    
    def mulitply(self):
        return self.par01 * self.par02

    def divide(self):
        return self.par01 / self.par02