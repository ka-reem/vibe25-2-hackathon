import { NextResponse } from 'next/server'
import { exec } from 'child_process'
import { promisify } from 'util'
import { join } from 'path'

const execAsync = promisify(exec)

export async function GET() {
  try {
    const pythonDir = join(process.cwd(), '..')
    
    // Simple Python script to load person data
    const pythonScript = `
import json
import os
try:
    with open('person_data.json', 'r') as f:
        data = json.load(f)
    print("SUCCESS:" + json.dumps(data))
except Exception as e:
    print("ERROR:" + str(e))
`
    
    const { stdout } = await execAsync(`python3 -c "${pythonScript}"`, {
      cwd: pythonDir
    })
    
    if (stdout.startsWith('SUCCESS:')) {
      const data = JSON.parse(stdout.substring(8))
      return NextResponse.json({ 
        success: true,
        person_data: data
      })
    } else {
      return NextResponse.json({ 
        success: false,
        error: 'No person data found'
      })
    }
  } catch (error) {
    return NextResponse.json({ 
      success: false,
      error: 'Failed to load person data'
    }, { status: 500 })
  }
}
