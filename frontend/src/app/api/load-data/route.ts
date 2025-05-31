import { NextResponse } from 'next/server'
import { readFile } from 'fs/promises'
import { join } from 'path'

export async function GET() {
  try {
    const pythonDir = join(process.cwd(), '..')
    const personDataPath = join(pythonDir, 'person_data.json')
    
    try {
      const fileContent = await readFile(personDataPath, 'utf-8')
      const personData = JSON.parse(fileContent)
      
      return NextResponse.json({
        success: true,
        person_data: personData
      })
    } catch (fileError) {
      // File doesn't exist or invalid JSON
      return NextResponse.json({
        success: false,
        person_data: null,
        message: 'No person data found'
      })
    }
  } catch (error) {
    console.error('Load data API error:', error)
    return NextResponse.json({
      error: 'Internal server error'
    }, { status: 500 })
  }
}