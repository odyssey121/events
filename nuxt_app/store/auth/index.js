
export const actions = {

    authenticateUser(vuexContent, payload) {
        const { email, password1, password2, isLogin } = payload;
        let authUrl = "";
        let sendData = {};
        if (isLogin) {
            authUrl = "/api/auth/login/";
            sendData = { email, password: password1 }
        } else {
            authUrl = "/api/auth/register/";
            sendData = { email, password1, password2 }
        }
        return this.$axios.$post(authUrl, sendData)
            .then(({ key }) => {
                vuexContent.commit('SET_TOKEN', key);
                localStorage.setItem('events_spa_token', key);

            });

    },

    checkAuth(vuexContent, req) {

        token = localStorage.getItem('events_spa_token');

        if (!token || !vuexContent.state.auth.user) {
            vuexContent.dispatch('unregister');
        }
    },
    unregister(vuexContent, _payload) {
        return new Promise((resolve, rej) => {
            vuexContent.commit('CLEAR_TOKEN')
            localStorage.removeItem('events_spa_token');
            resolve(true)
        })


    },
    getUser(vuexContent, _payload) {
        const getUserUrl = "/api/auth/user/";
        const token = localStorage.getItem('events_spa_token');
        this.$axios.setToken(`Token ${token}`);
        return this.$axios.$get(getUserUrl)
            .catch(err => {
                console.log('SET_USER_AND_TOKEN_ERROR => ', err);

            })
            .then(user => {
                if (user) {
                    vuexContent.commit('SET_USER', user);
                }
            }).then(() => vuexContent.commit('SET_TOKEN', token))

    }
}

export const mutations = {
    SET_TOKEN(state, token) {
        state.token = token;
    },
    SET_USER(state, user) {
        state.user = user;
    },
    CLEAR_TOKEN(state, _payload) {
        state.token = null;
        state.user = null;
    },
    CREATE_POST(state, post) {
        state.posts.push(post)
    },
    EDIT_POST(state, post) {
        let index = state.posts.findIndex(record => record.id === post.id)
        if (index >= 0) {
            state.posts[index] = { ...post }
        }


    }
}

export const getters = {
    getUser: (state, _getters) =>
        state.user
    ,
}


export const state = () => ({ user: null, token: null })














// export const mutations = {
//     SET_TOKEN(state, token) {
//         state.token = token
//     },
//     CLEAR_TOKEN(state) {
//         state.token = null
//     }
// }

// export const getters = {
//     isAuth: (state, _getters) => state.token != null

// }