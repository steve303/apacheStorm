# Apache Storm - Word Count

This is the Python template for ***"Machine Problem 11: Apache Storm / FLux"*** in 2021 Spring semester. To make the previous URL continue to work, we don't change the name of repo yet (will do later), but just use this README as an explanation.

Clarifications and hints on MP11
Since we are going through a high volume on MP11, I will list below some common issues that are frequently encountered in this MP.

The general objective of this mp is to help you develop a simple but end-to-end stream processing pipeline, including both data processing and data storage. Redis, as an efficient in-memory database, is used to store the result in real-time, to enable the END-TO-END stream processing. Otherwise, even if your computation stage is efficient, storing the result can be your efficiency bottleneck.
It is running locally. No AWS is involved.
After you finishing the part D, the end-to-end topology is: file spout --> split bolt --> normalize bolt --> word count bolt --> top-N bolt --> Redis store bolt.
The Redis bolt works in the most basic way. After you get the processing result (either the word-cout or top-N-list), you send it to the Redis store bolt. Then the Redis store bolt fetch the corresponding key-value pair, and store them under the given hashkey in the LOCAL Redis server.

I will use Python as the example, but most hints also apply to the Java templates.

Topology. The main challenge in defining the yaml files lies in the Redis part. As you can see in the tutorial, a RedisStoreBolt takes two arguments:
poolConfig: We have already defined the poolConfig in the template. 
You can set the configs here, e.g., file names, N, by defining a new key-value pair. You can get what you set by conf['your.config.name'] in your Python files.
storeMapper: You need to define the storeMapper under "components", besides the "poolConfig". The className for storeMapper is "edu.illinois.storm.*StoreMapper".
For the Part-a ~ Part-c, you need to use the WordCountStoreMapper, while for Part-d, you need to use the TopNStoreMapper.
Please note that the class names used here correspond to the Java files you need to finish. These two Java files are pretty simple. You just need one line to return the corresponding field in the tuple for both getKeyFromTuple and getValueFromTuple functions.
Remember to use the TopNStoreMapper for your Part-d otherwise you will get the error of "Cannot find your answer in Redis". 
The Redis hash key is set here as contructorArgs. Remember to use the correct hash key for each part.
redis bolt: After defining the two components, you can define the redis store bolt using the above two components as the constructorArgs. The ClassName is "org.apache.storm.redis.bolt.RedisStoreBolt". 
This is the ultimate bolt you use in the topology to connect with other bolts, while the above two are just the components.
You pass the poolConfig and storeMapper as constructorArgs by Reference. You can learn more about Reference from the Flux tutorial.
Please check carefully and ensure that the ids you defined for spout/bolts are the same ones you used in defining the streams.
Make sure the output fields you defined for word_count_bolt are same as the keys you extract in the WordCountStoreMapper.java. Similarly, make sure the output fields you defined for topN_bolt are same as the keys you extract in the TopNStoreMapper.java. Otherwise, the Redis server will not be able to find your answer, either.
Grouping: You need to think about which grouping method to use for each stream. You don't need the args if you choose to group by SHUFFLE. SHUFFLE is just shuffle. If you group by FIELDS, please only use one field, like ["word"], but not ["word", "count"].
Parallelism: Setting the parallelism larger than 1 can help improve your efficiency, but only if the job of the bolt can be parallel. I suggest to use 1 for spout, top-n-bolt, and redis-store-bolt.
random_sentence_spout:
Do not remove the sleep function we put outside the TODO part.
file_reader_spout:
Do not call readlines() inside nextTuple function, because you will read the whole file everytime the function is called.
Only read and process one line in the nextTuple function. If the line is valid, emit it; otherwise, sleep for 1 second to avoid a busy-loop.
It is fine either you close the file or not after reaching the EOF.
If you close the file, you have to explicitly set a flag so that you will never try to read the next line again but just directly sleep for 1 second in future calls.
If you don't close the file, you can contine to read the next line in future calls of nextTuple, which will just return an empty string every time. Then you can correspondingly sleep for 1 second.
Do not sleep for 1 second before the EOF, which will make your code too slow to pass the autograder.
split_sentence_bolt:
Use EXACTLY the provided pattern inside the re.split function to split the sentence and emit the word one by one.
normalizer_bolt:
Nothing special. Just make the word lower case and emit it if it is not in the common_words.
word_count_bolt:
I suggest you to convert the count to string before emitting, so that your WordCountStoreMapper can directly extract the value field as a string. Converting the Long to String inside *StoreMapper seems to not work very well from previous threads.
top_n_finder_bolt:
First, remember to convert the count to int before comparison, if you followed my previous suggestion.
You have to take care of the algorithm efficiency in this bolt. Some brute force methods will not pass the autograder. For example, you can not just store the count for each word, and call the most_common function of Counter to return the N most frequent words.
One algorithm (probably not the only one) that passed the autograder:
Maintain a heap to store the top-N words. Include other assistive data structures (like a dict or map) as well if you need.
If a new (word, count) arrives, first check whether the word is already in the top-N heap. If yes and the count is larger, update its count.
If the new word is not in the top-N heap, check whether the heap is full (i.e., it already has N elements):
If no, just add the new word.
If yes, use the new word to replace the word with the least count in the top-N heap.
Remember to convert the top-N word list to a string, before emitting the result. Your key should be "top-N", not "top-10".
Please read this thread carefully and see if it can resolve your issue. 

Thanks,

CS498 CCA Staff
