<template lang="html">
   <section id="blog-list-content">
      <h1>Blog</h1>
      <nav class="nav">
        <menu class="nav__controls">
          <!-- <icon class="nav__icon" use="#filter"></icon> -->

          <li v-for="(active, menu) in menus" class="nav__label"
            :class="{
              'nav__label--active' : active,
              'nav__label--filter': activeFilters[menu].length
            }" @click="setMenu(menu, active)">
              {{ menu }}
          </li>

          <li class="nav__label nav__label--clear" @click="clearAllFilters">Clear all</li>
        </menu>

      </nav>

       <transition-group name="dropdown" tag="section" class="dropdown" :style="dropdown">
        <menu v-for="(options, filter) in filters" class="filters"
          v-show="menus[filter]" ref="menu" :key="filter">
          <!-- <h3>{{ options }}</h3>
          <h4>{{ filters }}</h4> -->
          <template>
            <li v-for="(active, option) in options" class="filters__item"
              :class="{ 'filters__item--active': active }"
              @click="setFilter(filter, option)">
              {{ option }}
            </li>
          </template>
        </menu>
      </transition-group>

      <transition-group name="company" tag="ul" class="content__list" appear>
         <!-- https://github.com/SortableJS/Vue.Draggable/issues/144 - for work.id/key issues -->

         <li v-for="post in list" :key="post.id">
            <figure>
              <router-link :to="/blog/ + post.slug">
               <img :src="'/images/' + post.featured_image" alt="">
                 <figcaption class="company__info">
                  <h2 class="overlay company__name">
                      {{ post.title}}
                  </h2>
                </figcaption>
               </router-link>
            </figure>

          <ul class="company__details">
             <li class="company__data">
               <label class="company__label">Category</label>
                {{ post.category }}
             </li>

             <li class="company__data">
               <label class="company__label">Tags</label>
               <div v-for="tag in post.keywords" class="company__rating">
                 <h6>{{ tag }}</h6>
               </div>
             </li>
          </ul>
       </li>
    </transition-group>
</section><!--#blog-post-list-->

</template>

<script>
import Axios from 'axios';

export default {
   data: function() {
         return {
               dropdown: { height: 0 },
               filters: { tags: {}, categories: {}},
               menus: { tags: false, categories: false },
               dropdown: { height: 0 },
               filters: { tags: {}, categories: {} },
               menus: { tags: false, categories: false },
               posts: [],
               post: {
                  id: '',
                  title: '',
                  body: '',
                  slug: '',
                  excerpt: '',
                  category: {
                     name: ''
                  },
                  tags: [],
                  tag: {
                     name: ''
                  }
               }
         }
      },
      components: {
         'icon': { template: '<svg><use :xlink:href="use"/></svg>', props: ['use'] }
      },
      computed: {
       activeMenu: function activeMenu() {
         var _this = this;

         return Object.keys(this.menus).reduce(function ($$, set, i) {
           return _this.menus[set] ? i : $$;
         }, -1);
       },
       list: function list() {
         var _this2 = this;

         var _activeFilters = this.activeFilters,
             categories = _activeFilters.categories,
             tags = _activeFilters.tags;


         return this.posts.filter(function (_ref) {
           var category = _ref.category,
               keywords = _ref.keywords;

           if (categories.length && !~categories.indexOf(category)) return false;
           return !tags.length || tags.every(function (cat) {
             return ~keywords.indexOf(cat);
           });
         });
       },
       activeFilters: function activeFilters() {
         var _filters = this.filters,
             categories = _filters.categories,
             tags = _filters.tags;

         return {
           categories: Object.keys(categories).filter(function (c) {
             return categories[c];
           }),
           tags: Object.keys(tags).filter(function (c) {
             return tags[c];
           })
         };
      },
      replaceFilterName: function replaceFilterName() {

         const menuItems = document.querySelectorAll('.nav__label');

         menuItems[1].innerText = 'Categories';
      }
     },
     methods: {
       setFilter: function setFilter(filter, option) {
         var _this4 = this;
         if (filter === 'categories') {
           this.filters[filter][option] = !this.filters[filter][option];
        } else if (filter === 'tags') {
           this.filters[filter][option] = !this.filters[filter][option];
        } else {
           setTimeout(function () {
             _this4.clearFilter(filter, option, _this4.filters[filter][option]);
           }, 100);
         }
       },
       clearFilter: function clearFilter(filter, except, active) {
         var _this5 = this;

           Object.keys(this.filters[filter]).forEach(function (option) {
             _this5.filters[filter][option] = except === option && !active;
           });
       },
       clearAllFilters: function clearAllFilters() {
         Object.keys(this.filters).forEach(this.clearFilter);
       },
       setMenu: function setMenu(menu, active) {
         var _this6 = this;

         Object.keys(this.menus).forEach(function (tab) {
           _this6.menus[tab] = !active && tab === menu;
         });
      }
     },
     watch: {
       activeMenu: function activeMenu(index, from) {
         var _this3 = this;

         if (index === from) return;

         this.$nextTick(function () {
           if (!_this3.$refs.menu || !_this3.$refs.menu[index]) {
             _this3.dropdown.height = 0;
           } else {
             _this3.dropdown.height = _this3.$refs.menu[index].clientHeight + 100 + 'px';
           }
         });
       }
     },
       created() {
          var _this7 = this;
           Axios.get('/posts').then(response => this.posts = response.data.data).then(function (posts) {
              _this7.posts = posts;
              console.log(posts);
              posts.forEach(function (_ref2) {
                var category = _ref2.category,
                    keywords = _ref2.keywords;

                _this7.$set(_this7.filters.categories, category, false);

                keywords.forEach(function (tag) {
                  _this7.$set(_this7.filters.tags, tag, false);
                });
              });
            });

           //then(response => console.log(response.data.data));
       }
}

</script>

<style lang="css" scoped>
nav ul li {
   cursor: pointer;
}

.company {
  position: relative;
  width: calc(100% / 2 - 1rem);
  display: inline-flex;
  flex-direction: column;
  justify-content: space-between;
  margin-left: 1rem;
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-radius: 6px;
  background-color: white;
  box-shadow: 0 0 0 1px #c5d0d1;
  -webkit-backface-visibility: hidden;
          backface-visibility: hidden;
  -webkit-transform-origin: 10% 50%;
          transform-origin: 10% 50%;
  z-index: 1;
}
@media (min-width: 800px) {
  .company {
    width: calc(100% / 3 - 1rem);
  }
}
.company-move {
  transition: all 600ms ease-in-out 50ms;
}
.company-enter-active {
  transition: all 300ms ease-out;
}
.company-leave-active {
  transition: all 200ms ease-in;
  position: absolute;
  z-index: 0;
}
.company-enter, .company-leave-to {
  opacity: 0;
}
.company-enter {
  -webkit-transform: scale(0.9);
          transform: scale(0.9);
}
.company__data {
  line-height: 1.3;
}
.company__label {
  font-size: 0.8rem;
}
.company__rating {
  text-align: center;
}
.company__info {
  text-align: center;
}
.company__logo {
  width: 3rem;
  height: 3rem;
  margin: 0 auto;
}
.company__name {
  height: 2.5rem;
  font-size: 1.3rem;
  font-weight: 200;
  color: white;
  text-align: center;
}
.company__slogan {
  height: 2rem;
  text-align: center;
  font-weight: 400;
  text-transform: capitalize;
}
.company__details {
  justify-content: space-between;
  margin-top: 1.5rem;
  background-color: rgba(197, 208, 209, 0.1);
  border-top: 1px solid #c5d0d1;
}
.company__country:hover {
  text-decoration: underline;
  cursor: pointer;
}

.nav {
  display: flex;
  justify-content: center;
  align-items: center;
  white-space: nowrap;
  margin: 0;
  padding: 0;
  border-bottom: 1px solid #c5d0d1;
}
.nav__controls {
  display: flex;
}
.nav__icon {
  width: 1rem;
  height: 1rem;
  fill: currentColor;
}
.nav__label {
  position: relative;
  margin-left: 1rem;
  text-transform: capitalize;
  z-index: 1;
  cursor: pointer;
}
.nav__label::after {
  content: '\00d7';
  display: inline-block;
  color: transparent;
  width: 0.5rem;
  font-weight: 400;
  -webkit-transform: scale(0);
          transform: scale(0);
  transition: -webkit-transform 150ms ease-in-out;
  transition: transform 150ms ease-in-out;
  transition: transform 150ms ease-in-out, -webkit-transform 150ms ease-in-out;
}
.nav__label--clear {
  color: #f68185;
  opacity: 0;
  -webkit-transform: translate3d(-25%, 0, 0);
          transform: translate3d(-25%, 0, 0);
  pointer-events: none;
  transition: all 275ms ease-in-out;
}
.nav__label--filter ~ .nav__label--clear {
  opacity: 1;
  -webkit-transform: translate3d(0, 0, 0);
          transform: translate3d(0, 0, 0);
  pointer-events: auto;
}
.nav__label--filter::after, .nav__label--active::after {
  -webkit-transform: scale(1);
          transform: scale(1);
}
.nav__label--filter::after {
  content: '\2022';
  color: #46d2c4;
}
.nav__label--active::after {
  content: '\00d7';
  color: #f68185;
}

.dropdown {
  position: relative;
  height: 0;
  overflow: hidden;
  transition: height 350ms;
}
.dropdown::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1rem;
  background-image: linear-gradient(to top, white, rgba(255, 255, 255, 0));
}
.dropdown-enter, .dropdown-leave-to {
  opacity: 0;
}
.dropdown-leave, .dropdown-enter-to {
  opacity: 1;
}
.dropdown-enter-active, .dropdown-leave-active {
  position: absolute;
  width: 100%;
  transition: opacity 200ms ease-in-out;
}
.dropdown-enter-active {
  transition-delay: 100ms;
}

.filters {
  padding: 0 1rem;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
}
.filters__item {
  margin-top: 0.5rem;
  margin-right: 0.5rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid #c5d0d1;
  border-radius: 6px;
  font-size: 0.8rem;
  line-height: 1.35;
  cursor: pointer;
  transition: all 275ms;
}
.filters__item:hover {
  border-color: #09021d;
}
.filters__item--active {
  color: white;
  border-color: #09021d;
  background-color: #09021d;
}
</style>
