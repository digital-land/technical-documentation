
1. **Create csv file in root and populate**  
   To merge duplicate entities, we make use of the add-redirections command. For this, you will need to have a csv file with the entities you want to merge (we’ll name it `entity-merge.csv` for this explanation) . Imagine that  a `conservation-area` has duplicate entities, one with the entity number 3032307 and the other with number 3033940\. We want to combine both together as they refer to the same entity. We will essentially be redirecting references of 3032307 to 3033940 

   The csv file would look like this:

```
entity_source, entity_destination
3032307,3033940
```

2. **Run add-redirection script**

	Assuming the collection name is ‘conservation-area’, run the command in a virtual environment like so:

```
digital-land add-redirection ./entity-merge.csv -p ./pipeline/conservation-area
```

3. **Check result**

The command in step 2 should have added an entry in corresponding pipeline `old-entity.csv` file like so:

```
old-entity,status,entity
3032307,301,3033940
```

Once verified, the updated old-entity.csv file should then be pushed and merged.
