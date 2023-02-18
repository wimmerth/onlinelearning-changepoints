import datetime
import csv


if __name__ == "__main__":
    data = csv.reader(open("datasets/airline_passengers.csv", "r"))
    # skip the header
    next(data)

    print(sum([1 for row in data]))

    # data = sorted(data, key=lambda x: datetime.datetime.strptime(x[0], "%m/%d/%Y").timestamp())

    # write the dates and the total number of passengers in a new file
    # with open("datasets/brent_crude_oil.csv", "w") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["day", "DPB"])
    #     for row in data:
    #         writer.writerow(row)

