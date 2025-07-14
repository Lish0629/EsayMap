// src/utils/callGPService.js

/**
 * 通用 ArcGIS GP 服务调用函数
 * @param {string} gp_url - GP服务的完整URL（不含 /execute）
 * @param {Object} params - GP服务的输入参数（需符合ArcGIS Server要求）
 * @returns {Promise<Object>} - 返回GP服务执行结果
 */
export async function callGPService(gp_url, params) {
  const fullUrl = `${gp_url}/execute`

  try {
    const response = await fetch(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    })

    if (!response.ok) {
      const errText = await response.text()
      throw new Error(`GP服务调用失败: ${response.status} ${errText}`)
    }

    const result = await response.json()
    return result
  } catch (error) {
    console.error('GP服务调用错误：', error)
    throw error
  }
}
