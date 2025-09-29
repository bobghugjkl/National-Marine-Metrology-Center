<template>
    <div class="sidebar">
        <el-menu
            class="sidebar-el-menu"
            :default-active="onRoutes"
            :collapse="sidebar.collapse"
            :background-color="sidebar.bgColor"
            :text-color="sidebar.textColor"
            router
        >
            <template v-for="item in filteredMenuData">
                <template v-if="item.children">
                    <el-sub-menu :index="item.index" :key="item.index" v-permiss="item.id">
                        <template #title>
                            <el-icon>
                                <component :is="item.icon"></component>
                            </el-icon>
                            <span>{{ item.title }}</span>
                        </template>
                        <template v-for="subItem in item.children">
                            <el-sub-menu
                                v-if="subItem.children"
                                :index="subItem.index"
                                :key="subItem.index"
                                v-permiss="item.id"
                            >
                                <template #title>{{ subItem.title }}</template>
                                <el-menu-item
                                    v-for="(threeItem, i) in subItem.children"
                                    :key="i"
                                    :index="threeItem.index"
                                >
                                    {{ threeItem.title }}
                                </el-menu-item>
                            </el-sub-menu>
                            <el-menu-item v-else :index="subItem.index" v-permiss="item.id">
                                {{ subItem.title }}
                            </el-menu-item>
                        </template>
                    </el-sub-menu>
                </template>
                <template v-else>
                    <el-menu-item :index="item.index" :key="item.index" v-permiss="item.id">
                        <el-icon>
                            <component :is="item.icon"></component>
                        </el-icon>
                        <template #title>{{ item.title }}</template>
                    </el-menu-item>
                </template>
            </template>
        </el-menu>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useSidebarStore } from '../store/sidebar';
import { useRoute } from 'vue-router';
import { menuData } from '@/components/menu';


// Assume userPermissions is fetched from a store or API
const userPermissions = [ '0', '01','02','03','1', '11', '12', '13','2' ,'21','22','23','24','25','26','27','28','29','3','31','32','33','34','4','41','42']; // Example permissions

// Filter menuData based on user permissions
const filteredMenuData = computed(() => {
  const filterMenu = (items: any[], permissions: string[]): any[] => {
    return items
      .filter((item) => {
        // Include item if its ID is in permissions or it has permitted children
        if (permissions.includes(item.id)) return true;
        if (item.children) {
          const hasPermittedChildren = item.children.some((child: any) =>
            permissions.includes(child.id) || (child.children && child.children.some((subChild: any) => permissions.includes(subChild.id)))
          );
          return hasPermittedChildren;
        }
        return false;
      })
      .map((item) => {
        // Recursively filter children if they exist
        if (item.children) {
          return {
            ...item,
            children: filterMenu(item.children, permissions),
          };
        }
        return item;
      });
  };

  return filterMenu(menuData, userPermissions);
});

const route = useRoute();
const onRoutes = computed(() => {
    return route.path;
});

const sidebar = useSidebarStore();
</script>

<style scoped>
.sidebar {
    display: block;
    position: absolute;
    left: 0;
    top: 70px;
    bottom: 0;
    overflow-y: scroll;
}

.sidebar::-webkit-scrollbar {
    width: 0;
}

.sidebar-el-menu:not(.el-menu--collapse) {
    width: 250px;
}

.sidebar-el-menu {
    min-height: 100%;
}
</style>
