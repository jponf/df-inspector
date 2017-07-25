
(println "Reading dummy csv")
(let df (read_csv "samples/dummy.csv"))

(println "Data frame content")
(println df)

(println)
(println "Extracting first and second column")
(let df12 ($ 1 2 df))

(println "Printing first and second column")
(println df12)
