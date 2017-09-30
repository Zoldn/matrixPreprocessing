<template>
    <div id="app">
        <preloader></preloader>
        <div class="header">
            <div class="flex-center">
                <div class="icon_logo" style="margin-top: 5px;"></div>
                <div class="route-header">
                    {{header}}
                </div>
            </div>
            <div class="flex-center">
                <drop-down class="w135px" v-if="!logged_in">
                    <div slot="header" class="dd-header top-menu-button button">Регистрация</div>
                    <div slot="element" @click="goTo('reg-advertiser')" class="dd-elem">Рекламодатель</div>
                    <div slot="element" @click="goTo('reg-specialist')" class="dd-elem">Специалист</div>
                </drop-down>
                <login v-if="!logged_in" style="float:right">

                </login>
                <button class="top-menu-button letter-spaced" v-else @click="logout(); alert('ДРУГАЯ КНОПКА!!!')">
                    Выйти
                </button>
            </div>
        </div>
        <div class="menu" v-if="logged_in">
            <div class="menu__elem" v-for="(m, $index) in menu" @click="goTo(m.url)" :class="{active: $index === 0}">
                <div class="menu__image" :class="[m.cl, {active: $index === 0}]"></div>
                <div class="menu__text caps">{{m.name}}</div>
            </div>
            <div class="menu__exit">
                <div class="menu__text letter-spaced" @click="logout">Выход</div>
            </div>
        </div>
        <div :class="{'work-area': logged_in, 'common-area': !logged_in}">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import Preloader from '@/components/pre-loader';
    import Login from '@/components/login';
    import DropDown from '@/components/drop-downs/drop-down-slot';

    export default {
        name: 'app',
        components: {Preloader, Login, DropDown},
        data: function () {
            return {
                menu: [
                    {
                        name: 'Проекты',
                        cl: 'n1',
                        url: 'projects'
                    },
                    {
                        name: 'Биржа',
                        cl: 'n2'
                    },
                    {
                        name: 'Задачи',
                        cl: 'n3'
                    },
                    {
                        name: 'Профиль',
                        cl: 'n4'
                    }
                ]
            };
        },
        methods: {
            logout() {
                this.$store.commit('logout');
                this.$router.push({name: 'index'});
            },
            goTo(url) {
                !url || (this.$router.push({name: url}));
            },
            alert(val) { // just a friendly joke
                alert(val);
            }
        },
        computed: {
            logged_in() {
                return !!this.$store.getters.user;
            },
            header() {
                return this.$route.meta.header || '';
            }
        }
    }
</script>

<style lang="postcss" scoped>
    @import "@styles/constants.pcss";

    #app {
        margin: 0;
        height: 100%;
        width: 100%;
    }

    .header {
        height: 50px;
        left: 0;
        right: 0;
        top: 0;
        position: fixed;
        z-index: 1000;
        background-color: #40444f;
        color: #fff;

        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .menu {
        background: #fff;
        position: fixed;
        z-index: 999;
        padding-top: 50px;
        left: 0;
        top: 0;
        bottom: 0;
        width: 83px;
        border-right: 1px solid var(--border-color);

    .menu__elem {
        width: 100%;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-bottom: 1px solid var(--border-color);
        align-items: center;
        color: var(--dark-blue);

    &
    :not(.active) {
        background: #FCFCFC;
    }

    &
    :hover {
        cursor: pointer;
    }

    .menu__image {
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;

    &
    .n1 {
        background-image: url('images/main-menu/main_projects.svg');
        width: 40px;
        height: 40px;
        background-size: 35px 38px;

    &
    .active {
        background-image: url('images/main-menu/main_projects_selected.svg');
    }

    }
    &
    .n2 {
        background-image: url('images/main-menu/main_birja.svg');
        width: 40px;
        height: 40px;
        background-size: 35px 37px;

    &
    .active {
        background-image: url('images/main-menu/main_birja_selected.svg');
    }

    }
    &
    .n3 {
        background-image: url('images/main-menu/main_tasks.svg');
        width: 40px;
        height: 40px;
        background-size: 38px 38px;

    &
    .active {
        background-image: url('images/main-menu/main_tasks_selected.svg');
    }

    }
    &
    .n4 {
        background-image: url('images/main-menu/main_profile.svg');
        width: 40px;
        height: 40px;
        background-size: 40px 37px;

    &
    .active {
        background-image: url('images/main-menu/main_profile_selected.svg');
    }

    }
    }
    }
    .menu__exit {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding-bottom: 20px;
        text-align: center;

    &
    :hover {
        cursor: pointer;
    }

    }
    .menu__text {
        margin-top: 16px;
        text-transform: uppercase;
        font-size: 12px;
    }

    }

    .route-header {
        font-size: 19px;
        margin-left: 25px;
        padding-bottom: 3px;
        letter-spacing: 1px;
        font-weight: bold;
    }

    .work-area {
        padding: 50px 0 0 83px;
        width: 100%;
        height: 100%;
    }

    .common-area {
        padding: 50px 3vw 0;
        width: 100%;
        height: 100%;
    }
</style>
