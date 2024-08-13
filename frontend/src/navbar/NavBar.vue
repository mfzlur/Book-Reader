<template>
    <nav class="navbar" v-if="showLibrarianNavbar">
        <div class="container">
            <div class="navbar-menu" v-if="isAuthenticated">
                
                    <router-link v-if="isAuthenticated" to="/librarian/dashboard" class="navbar-item">Home</router-link>

                    <router-link v-if="isAuthenticated" to="/librarian/stats" class="navbar-item">Stats</router-link>

                    <router-link v-if="isAuthenticated" to="/add/book" class="navbar-item">Add Book</router-link>

                    <router-link v-if="isAuthenticated" to="/add/section" class="navbar-item">Add Section</router-link>

                    <router-link v-if="isAuthenticated" to="/pending/requests" class="navbar-item">Requests</router-link>

                    <a v-if="isAuthenticated" @click="logout" class="navbar-item">Logout</a>
                
                <div class="navbar-search">
                    <input type="text" v-if="isAuthenticated" placeholder="type book name, section name or author name..."
                        v-model="query" class="search-box" @keyup.enter="search">
                </div>
            </div>
        </div>
    </nav>
    <nav class="navbar" v-if="showRegularNavbar">
        <div class="container">
            <div class="navbar-menu" v-if="isAuthenticated">
                
                    <router-link v-if="isAuthenticated" to="/user/dashboard" class="navbar-item">Home</router-link>

                    <router-link v-if="isAuthenticated" to="/my/books" class="navbar-item">My Books</router-link>

                    <router-link v-if="isAuthenticated" to="/all/books" class="navbar-item">All Books</router-link>

                    <a v-if="isAuthenticated" @click="logout" class="navbar-item">Logout</a>
                
                <div class="navbar-search">
                    <input type="text" v-if="isAuthenticated" placeholder="type book name, section name or author name..."
                        v-model="query" class="search-box" @keyup.enter="search">
                </div>
            </div>
        </div>
    </nav>
    

    
</template>

<script>
import { mapState } from 'vuex';
import store from '../store/index';

export default {
    name: "NavBar",
    data() {
        return {
            user: JSON.parse(localStorage.getItem('user')),
            query: ''
        };
    },
    computed: {
        ...mapState(['isAuthenticated', 'showRegularNavbar', 'showLibrarianNavbar']),
    },
    methods: {
        logout() {
            const accessToken = localStorage.getItem('access_token');
            this.$axios.post("/api/logout", null, {
                headers: {
                    Authorization: `Bearer ${accessToken}`
                }
            })
                .then(() => {
                    store.commit('setAuthenticated', false);
                    localStorage.clear()
                    

                    this.$router.push("/login");

                })
                .catch(error => {
                    console.error('Logout failed:', error);
                });
        },
        search() {
            if (this.query) {
                this.$router.push(`/search?q=${this.query}`);
            }
        },
    }

};
</script>

<style>
.navbar {
    background-color: #05386d;
    opacity: 0.9;
    border: 0;
    margin: 0 0 20px 0;
    padding: 0;
    text-decoration: none;
    position: fixed;
    top: 0;
    right: 0;
    left: 0;
    width: 100%;
    z-index: 100;
    box-shadow: 0 2px 4px rgba(75, 74, 74, 0.1);
    display: flex;
    align-items: right;
    justify-content: center;
    height: 80px;
    width: 100%;
}

.navbar-menu {
    display: flex;
    justify-content: flex-end;
    width: 100%;
}



.navbar-item {
    color: white;
    /* Updated color to white */
    font-family: Arial, sans-serif;
    text-decoration: none;
    padding: 10px;
    font-size: 16px;
    cursor: pointer;
    transition: transform 0.3s, background-color 0.3s;
    font-weight: bold;
    /* Added font-weight to make the text bolder */
    margin-right: 20px;
    width: 15%;
    /* border: 1px solid #0e2ee4; */
    border-radius: 5px;
    background-color: #5284ba;
}



.navbar-search {
    width: 70%;
    height: 45px;
    border-radius: 5px;
    border: 1px solid #05386d;
    padding: 5px;
    font-size: 16px;
    margin-right: 0px;
    
}

.navbar-item:hover {
    transform: scale(1.1);
    background-color: #baebed;
}
</style>