def fetchByQyery(self, query):
    fetchQuery = self.connection.execute(f"SELECT * FROM {query}")
        
    for data in fetchQuery.fetchall():
        print(data)