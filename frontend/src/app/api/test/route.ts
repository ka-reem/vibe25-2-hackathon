import { NextResponse } from 'next/server'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

export async function GET() {
  try {
    // Super simple test - just run Python and return a message
    const { stdout } = await execAsync('python3 -c "print(\\"Hello from Python!\\")"')
    
    return NextResponse.json({ 
      success: true,
      message: stdout.trim()
    })
  } catch (error) {
    return NextResponse.json({ 
      success: false,
      error: 'Python execution failed'
    }, { status: 500 })
  }
}
