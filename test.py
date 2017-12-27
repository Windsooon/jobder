{
  search(query: "language:JavaScript stars:>3000", type: REPOSITORY, first: 100, after: "Y3Vyc29yOjE=") {
    repositoryCount
    edges {
      cursor
      node {
        ... on Repository {
          name
          descriptionHTML
          stargazers {
            totalCount
          }
          updatedAt
        }
      }
    }
    pageInfo {
      startCursor
      hasNextPage
    }
  }
}
