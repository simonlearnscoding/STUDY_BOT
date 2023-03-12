import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()

// A `main` function so that we can use async/await
async function main() {
    deleteAllTables()
}

async function deleteAllTables() {
    // Get a list of all tables in the database
    // get names of all tables
    const tables = await prisma.$queryRaw`SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'`
    // for tables in table
    for (const table of tables) {
        // drop table
        await prisma.$queryRaw`DROP TABLE ${table}`
    }
}

console.log('before main')
main()
.catch(e => { throw e})
    .finally(async () => {
    await prisma.$disconnect()
})


//is it easier to use prisma or waterline?