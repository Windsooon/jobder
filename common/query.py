def get_repos_query(user_name, num):
    num = str(num)
    return 'query {user(login: "' + user_name + '") {' + \
          '''name
          avatarUrl
          location
          websiteUrl
          email
          bio
          repositories(first:''' + num + ''', isFork: false, orderBy: {direction: DESC, field: STARGAZERS}) {
              edges {
                  node {
                      id
                      name
                      nameWithOwner
                      url
                      description
                      stargazers {
                        totalCount
                      }
                      primaryLanguage {
                          name
                      }
                  }
              }
          }
          repositoriesContributedTo(first:''' + num + ''', contributionTypes:[COMMIT,], orderBy: {direction: DESC, field: STARGAZERS}) {
              edges {
                  node {
                      id
                      name
                      nameWithOwner
                      url
                      description
                      stargazers {
                        totalCount
                      }
                      primaryLanguage {
                          name
                      }
                  }
              }
          }
        }}'''
