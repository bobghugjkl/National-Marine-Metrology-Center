<template>
    <div class="signature-pad-container">
        <div class="signature-header">
            <h3>手写签名</h3>
            <div class="signature-actions">
                <el-button @click="clearSignature" size="small">清除</el-button>
                <el-button @click="saveSignature" type="primary" size="small" :disabled="!hasSignature">
                    保存签名
                </el-button>
            </div>
        </div>
        
        <div class="signature-pad-wrapper">
            <canvas
                ref="signatureCanvas"
                class="signature-canvas"
                @mousedown="startDrawing"
                @mousemove="draw"
                @mouseup="stopDrawing"
                @mouseleave="stopDrawing"
                @touchstart="startDrawing"
                @touchmove="draw"
                @touchend="stopDrawing"
            ></canvas>
        </div>
        
        <div v-if="signatureData" class="signature-preview">
            <h4>当前签名预览：</h4>
            <img :src="signatureData" alt="签名预览" class="signature-image" />
        </div>
    </div>
</template>

<script setup lang="ts" name="signature-pad">
import { ref, onMounted, nextTick } from 'vue';

const emit = defineEmits(['save']);

const signatureCanvas = ref<HTMLCanvasElement>();
const signatureData = ref<string>('');
const hasSignature = ref(false);

let isDrawing = false;
let ctx: CanvasRenderingContext2D | null = null;

onMounted(() => {
    nextTick(() => {
        if (signatureCanvas.value) {
            ctx = signatureCanvas.value.getContext('2d');
            if (ctx) {
                // 确保画布尺寸与显示尺寸一致
                const canvas = signatureCanvas.value;
                const rect = canvas.getBoundingClientRect();
                canvas.width = rect.width;
                canvas.height = rect.height;
                
                // 设置画布样式
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 2;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
            }
        }
    });
});

const startDrawing = (e: MouseEvent | TouchEvent) => {
    isDrawing = true;
    if (!ctx) return;
    
    e.preventDefault();
    
    let x, y;
    if (e instanceof MouseEvent) {
        x = e.offsetX;
        y = e.offsetY;
        console.log('Mouse start:', { offsetX: e.offsetX, offsetY: e.offsetY, clientX: e.clientX, clientY: e.clientY });
    } else {
        const rect = signatureCanvas.value!.getBoundingClientRect();
        x = e.touches[0].clientX - rect.left;
        y = e.touches[0].clientY - rect.top;
        console.log('Touch start:', { x, y, rect: rect });
    }
    
    ctx.beginPath();
    ctx.moveTo(x, y);
};

const draw = (e: MouseEvent | TouchEvent) => {
    if (!isDrawing || !ctx) return;
    
    e.preventDefault();
    
    let x, y;
    if (e instanceof MouseEvent) {
        x = e.offsetX;
        y = e.offsetY;
        console.log('Mouse draw:', { offsetX: e.offsetX, offsetY: e.offsetY });
    } else {
        const rect = signatureCanvas.value!.getBoundingClientRect();
        x = e.touches[0].clientX - rect.left;
        y = e.touches[0].clientY - rect.top;
    }
    
    ctx.lineTo(x, y);
    ctx.stroke();
    
    hasSignature.value = true;
};

const stopDrawing = () => {
    isDrawing = false;
};

const clearSignature = () => {
    if (!ctx || !signatureCanvas.value) return;
    
    ctx.clearRect(0, 0, signatureCanvas.value.width, signatureCanvas.value.height);
    signatureData.value = '';
    hasSignature.value = false;
};

const saveSignature = () => {
    if (!signatureCanvas.value) return;
    
    // 将画布内容转换为base64图片
    const dataURL = signatureCanvas.value.toDataURL('image/png');
    signatureData.value = dataURL;
    
    // 发送签名数据给父组件
    emit('save', dataURL);
};

// 暴露方法给父组件
defineExpose({
    clearSignature,
    saveSignature,
    getSignatureData: () => signatureData.value
});
</script>

<style scoped>
.signature-pad-container {
    border: 1px solid #e4e7ed;
    border-radius: 4px;
    padding: 20px;
    background: #fff;
}

.signature-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.signature-header h3 {
    margin: 0;
    color: #303133;
    font-size: 16px;
}

.signature-actions {
    display: flex;
    gap: 10px;
}

.signature-pad-wrapper {
    border: 2px dashed #dcdfe6;
    border-radius: 4px;
    background: #fafafa;
    margin-bottom: 15px;
}

.signature-canvas {
    display: block;
    width: 100%;
    height: 200px;
    cursor: crosshair;
    background: #fff;
}

.signature-preview {
    border-top: 1px solid #e4e7ed;
    padding-top: 15px;
}

.signature-preview h4 {
    margin: 0 0 10px 0;
    color: #606266;
    font-size: 14px;
}

.signature-image {
    max-width: 300px;
    max-height: 100px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    background: #fff;
}
</style>
