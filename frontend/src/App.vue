<template>
  <router-view />
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
});
</script>
<!-- 
<template>
  <div class="upload-container">
    <h1>Upload a file</h1>
    <input type="file" ref="fileInput" @change="handleFileUpload" />
    <button @click="uploadFile">Upload</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: "Up_load",
  data() {
    return {
      file: null, // 保存用户选择的文件
      message: "", // 显示上传结果信息
    };
  },
  methods: {
    // 处理文件上传
    handleFileUpload() {
      this.file = this.$refs.fileInput.files[0];
    },
    // 上传文件到后端
    uploadFile() {
      // 创建 FormData 对象
      let formData = new FormData();
      // 将文件添加到 FormData 对象中
      formData.append("file", this.file);
      // 发送 POST 请求，将 FormData 对象发送到后端的 /upload 接口
      axios
        .post("upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          // 上传成功后，显示成功信息
          this.message = response.data.message;
          // 清空文件选择框中的内容
          this.$refs.fileInput.value = "";
        })
        .catch((error) => {
          // 上传失败后，显示错误信息
          this.message = error.response.data.message;
        });
    },
  },
};
</script>

<style scoped>
.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  margin-top: 2rem;
}

input[type="file"] {
  margin-top: 1rem;
}

button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  border: none;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
}

p {
  margin-top: 1rem;
  font-weight: bold;
  color: red;
}
</style> -->
