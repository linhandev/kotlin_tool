import org.jetbrains.kotlin.gradle.dsl.KotlinMultiplatformExtension

buildscript {
    val kotlinVersion = project.findProperty("kotlinVersion")
    repositories {
        mavenLocal()
        maven("https://maven.eazytec-cloud.com/nexus/repository/maven-public/")
        maven("https://mirrors.tencent.com/nexus/repository/maven-tencent")
        mavenCentral()
        google()
    }
    dependencies {
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlinVersion")
    }
}

apply(plugin = "org.jetbrains.kotlin.multiplatform")

repositories {
    mavenLocal()
    maven("https://maven.eazytec-cloud.com/nexus/repository/maven-public/")
    maven("https://mirrors.tencent.com/nexus/repository/maven-tencent")
    mavenCentral()
    google()
}

configure<KotlinMultiplatformExtension> {
    ohosArm64 {
        binaries {
            sharedLib {
                baseName = "demo"
            }
        }
        compilations.getByName("main").cinterops.create("custom") {
            defFile(project.file("src/ohosArm64Main/cinterop/custom.def"))
            includeDirs(project.file("src/ohosArm64Main/cinterop/include"))
        }
        compilations.all {
            compilerOptions.options.optIn.add("kotlinx.cinterop.ExperimentalForeignApi")
        }
    }
}
