export default function ({ store, redirect }) {

    // console.log(context.store.getters['auth/getUser'])
    if (store.getters['auth/getUser'] === null) {
        redirect('/auth');
    }
}