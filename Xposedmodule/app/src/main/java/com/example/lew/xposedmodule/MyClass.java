package com.example.lew.xposedmodule;

/**
 * Created by Lew on 24/8/2017.
 */
import android.transition.Scene;

import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.XC_MethodHook;
import de.robv.android.xposed.callbacks.XC_LoadPackage.LoadPackageParam;

import static de.robv.android.xposed.XposedHelpers.findAndHookMethod;

public class MyClass implements IXposedHookLoadPackage {

    public void handleLoadPackage(final LoadPackageParam lpparam) throws Throwable {

        String targetPackage = "com.flappybird.tapping";
        String targetClass = "object.BestScore";
        String targetMethod = "reset";

        if(lpparam.packageName.equals(targetPackage)) {

            findAndHookMethod(targetClass, lpparam.classLoader, targetMethod,
                    new XC_MethodHook() {
                        @Override
                        protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                            System.out.println("METHOD HOOKED");
                        }
                    });
        }
    }

}