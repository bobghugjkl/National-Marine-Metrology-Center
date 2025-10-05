<template>
    <div>
        <!-- 表格工具栏 -->
        <div class="table-toolbar" v-if="hasToolbar">
            <div class="table-toolbar-left">
                <slot name="toolbarBtn"></slot>
            </div>
            <div class="table-toolbar-right flex-center">
                <template v-if="multipleSelection.length > 0">
                    <el-tooltip effect="dark" content="删除选中" placement="top">
                        <el-icon class="columns-setting-icon" @click="delSelection(multipleSelection)">
                            <Delete />
                        </el-icon>
                    </el-tooltip>
                    <el-divider direction="vertical" />
                </template>
                <el-tooltip effect="dark" content="刷新" placement="top">
                    <el-icon class="columns-setting-icon" @click="refresh">
                        <Refresh />
                    </el-icon>
                </el-tooltip>
                <el-divider direction="vertical" />
                <el-tooltip effect="dark" content="列设置" placement="top">
                    <el-dropdown :hide-on-click="false" size="small" trigger="click">
                        <el-icon class="columns-setting-icon">
                            <Setting />
                        </el-icon>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item v-for="c in columns">
                                    <el-checkbox v-model="c.visible" :label="c.label" />
                                </el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </el-tooltip>
            </div>
        </div>
        
        <!-- 表格容器：实现水平滚动的关键 -->
        <!-- 当表格内容宽度超出此容器时，会自动出现水平滚动条 -->
        <div class="table-container">
            <el-table class="mgb20" :style="{ width: '100%' }" border :data="tableData" :row-key="rowKey"
            @selection-change="handleSelectionChange" @row-click="handleRowClick" table-layout="auto">
            <template v-for="item in columns" :key="item.prop">
                <!-- el-table-column 的 :fixed 属性是实现列固定的关键 -->
                <!-- 直接使用 item.fixed 的值来设置固定列 -->
                <!-- 例如：fixed: 'left' 用于序号列，fixed: 'right' 用于操作列 -->
                <el-table-column v-if="item.visible" :prop="item.prop" :label="item.label" :width="item.width"
                    :type="item.type" :align="item.align || 'center'" :fixed="item.fixed">

                    <template #default="{ row, column, $index }" v-if="item.type === 'index'">
                        {{ getIndex($index) }}
                    </template>
                    <template #default="{ row, column, $index }" v-if="!item.type">
                        <slot :name="item.prop" :rows="row" :index="$index">
                            <template v-if="item.prop == 'operator'">
                                <div class="operator-buttons" @click.stop>
                                    <slot name="operator" :rows="row">
                                        <el-button type="warning" size="small" :icon="View" @click="viewFunc(row)">
                                            查看
                                        </el-button>
                                        <el-button type="primary" size="small" :icon="Edit" @click="editFunc(row)">
                                            编辑
                                        </el-button>
                                        <el-button type="danger" size="small" :icon="Delete" @click="delFunc(row)">
                                            删除
                                        </el-button>
                                    </slot>
                                </div>
                            </template>
                            <span v-else-if="item.formatter">
                                {{ item.formatter(row[item.prop]) }}
                            </span>
                            <span v-else>
                                {{ row[item.prop] }}
                            </span>
                        </slot>
                    </template>
                </el-table-column>
            </template>
            </el-table>
        </div>
        <el-pagination v-if="hasPagination" :current-page="currentPage" :page-size="pageSize" :background="true"
            :layout="layout" :total="total" @current-change="handleCurrentChange" />
    </div>
</template>

<script setup lang="ts">
import { toRefs, PropType, ref } from 'vue'
import { Delete, Edit, View, Refresh } from '@element-plus/icons-vue';
import { ElMessageBox } from 'element-plus';

const props = defineProps({
    // 表格相关
    tableData: {
        type: Array,
        default: []
    },
    columns: {
        type: Array as PropType<any[]>,
        default: []
    },
    rowKey: {
        type: String,
        default: 'id'
    },
    hasToolbar: {
        type: Boolean,
        default: true
    },
    //  分页相关
    hasPagination: {
        type: Boolean,
        default: true
    },
    total: {
        type: Number,
        default: 0
    },
    currentPage: {
        type: Number,
        default: 1
    },
    pageSize: {
        type: Number,
        default: 10
    },

    layout: {
        type: String,
        default: 'total, prev, pager, next'
    },
    delFunc: {
        type: Function,
        default: () => { }
    },
    viewFunc: {
        type: Function,
        default: () => { }
    },
    editFunc: {
        type: Function,
        default: () => { }
    },
    delSelection: {
        type: Function,
        default: () => { }
    },
    refresh: {
        type: Function,
        default: () => { }
    },
    changePage: {
        type: Function,
        default: () => { }
    },
    rowClickFunc: {
        type: Function,
        default: () => { }
    }
})

let {
    tableData,
    columns,
    rowKey,
    hasToolbar,
    hasPagination,
    total,
    currentPage,
    pageSize,
    layout,
} = toRefs(props)

columns.value.forEach((item) => {
    if (item.visible === undefined) {
        item.visible = true
    }
})

// 当选择项发生变化时会触发该事件
const multipleSelection = ref([])
const handleSelectionChange = (selection: any[]) => {
    multipleSelection.value = selection
}

// 当前页码变化的事件
const handleCurrentChange = (val: number) => {
    props.changePage(val)
}

// 行点击事件
const handleRowClick = (row: any, column: any) => {
    // 如果点击的是操作列，不触发跳转
    if (column && column.property === 'operator') {
        return;
    }
    props.rowClickFunc(row)
}

const handleDelete = (row) => {
    ElMessageBox.confirm('确定要删除吗？', '提示', {
        type: 'warning'
    })
        .then(async () => {
            props.delFunc(row);
        })
        .catch(() => { });
};

const getIndex = (index: number) => {
    return index + 1 + (currentPage.value - 1) * pageSize.value
}

</script>

<style scoped>
/* 表格容器样式：实现水平滚动的关键 */
.table-container {
    overflow-x: auto; /* 当内容超出容器宽度时，显示水平滚动条 */
    width: 100%; /* 确保容器占据可用宽度 */
    margin-bottom: 20px;
}

/* 响应式设计：当屏幕足够宽时，移除滚动条 */
@media (min-width: 1300px) {
    .table-container {
        overflow-x: visible; /* 宽屏时移除水平滚动条 */
    }
}

.table-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 10px;
}

.columns-setting-icon {
    display: block;
    font-size: 18px;
    cursor: pointer;
    color: #676767;
}

.operator-buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    flex-wrap: nowrap;
}

.operator-buttons .el-button {
    margin: 0;
}

/* 表格行悬停样式 */
:deep(.el-table tbody tr) {
    cursor: pointer;
}

:deep(.el-table tbody tr:hover > td) {
    background-color: #f5f7fa;
}
</style>
<style>
.table-header .cell {
    color: #333;
}
</style>