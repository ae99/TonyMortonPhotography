def pageinateRange(current, lastpage):
    firstpage = 1
    # If 10 or less pages, just return normal page numbers
    if lastpage <= 10:
        return list(range(firstpage, lastpage + 1))

    lowerBound = current - 5  # The first number to display
    upperBound = current + 4  # The last number

    # Check if the lower bound is lower than the first page number
    if lowerBound < firstpage:
        # if it is, give an extra "buffer" to the upper bound - always shows 10 numbers
        upperAdd = firstpage - lowerBound
        upperBound += upperAdd
        lowerBound = firstpage

    # Check if the upper bound set exceeds the number of pages
    if upperBound > lastpage:
        # if it is, give an extra "buffer" to the lower bound - always shows 10 numbers
        lowerAdd = lastpage - upperBound
        lowerBound += lowerAdd
        upperBound = lastpage

    return list(range(lowerBound,upperBound+1))


print(paginate(1,300))
