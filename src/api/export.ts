/**
 * 导出数据包API接口
 */
import request from '../utils/request'

/**
 * 导出任务数据包
 * @param taskName 任务名称
 * @returns Promise<Blob> 压缩包文件
 */
export function exportDataPackage(taskName: string): Promise<Blob> {
  return request({
    url: `/export/data-package/${encodeURIComponent(taskName)}`,
    method: 'GET',
    responseType: 'blob',
    headers: {
      'Accept': 'application/zip, application/octet-stream'
    }
  })
}
